#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
from datetime import datetime
from json import loads
import switchconfig_operation as switchconfig
import write2dashboard
from xml.dom.minidom import Document, parse
import xml.etree.ElementTree as et

passnumber = 0
failnumber = 0

def main():
    global  passnumber, failnumber
    #select case;
    basedir = (os.path.dirname(os.path.abspath(__file__)))
    #basedir = "C:\\Simon\\BannekerTest"
    filename = basedir+"\\TestCaseManagement.xlsx"
    xmlfile = basedir+"\\log\\"+"tmp.xml"
    htmlfile = basedir+"\\log\\"+"index.html"
    sw= switchconfig.SwitchConfigOperation(filename, 0)
    casecmd_list,casename_list, casenum_list = sw.getCaseInfo(4)
    caselines = sw.getTestCaseRowNumber(4)

    #handle history logfile, first copy , then delete
    os.system('del ' + basedir + "\\Report.xml " + r"/Q")
    os.system('del '+basedir +"\\log "+r"/Q")
    #run case;
    starttime = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
    time1 = datetime.now()
    for i in range(len(casecmd_list)):
        os.system(basedir+"\\"+casecmd_list[i]+" "+casenum_list[i])
    endtime = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
    time2 = datetime.now()
    duration = calduration(time1, time2)
    #get the case result;
    tmplog = basedir+"\\log\\"+"tmp.log"
    for index, line in enumerate(open(tmplog, 'r')):
        dicres = loads(line)
        if dicres['failnumber'] >= 1:
            #write the result back to excel;
            sw.setCellValue(caselines[index],6,"FAIL")
            sw.saveModify(filename)
        else:
            #write the result back to excel;
            sw.setCellValue(caselines[index],6,"PASS")
            sw.saveModify(filename)
    #compare result
    expectRes=sw.getTestResult(5)
    dectetRes=sw.getTestResult(6)
    for i in range(len(expectRes)):
        if expectRes[i]!=dectetRes[i]:
            failnumber+=1
        else:
            passnumber+=1

    #create report
    totalnumber = sw.getRowsLenth()-1
    notrunnumber = totalnumber-passnumber-failnumber
    hwversion = "RXDV3"
    swversion = "R5.0"
    phase = "PV"
    writeobj = write2dashboard.writetoreport(duration, starttime, endtime, totalnumber, passnumber, failnumber, notrunnumber, hwversion, swversion, phase)
    xmlpath = basedir+"\\log\\Report.xml"
    writeobj.writeInfoToXml(xmlpath)
    project = writeobj.output['project']
    sku = writeobj.output['sku']
    testjob = writeobj.output['testjob']
    brand = writeobj.output['brand']
    tester = writeobj.output['tester']
    logpath = basedir+"\\log"
    uploadpath = "C:\\JenkinsTestReports\\workspace\\"+project+"\\"+sku+"\\"+testjob+"\\"+starttime
    createReportXml(filename=xmlfile,brand=brand,project=project,sku=sku,testjob=testjob,duration=duration,starttime=starttime,\
                    endtime=endtime,testcasecount=totalnumber,pass_count=passnumber,fail_count=failnumber,norun_count=notrunnumber,\
                    hw_version=hwversion,sw_version=swversion,phase=phase)
    for idx, row in enumerate(open(tmplog, 'r')):
        dic_log = loads(row)
        ##dicres:{"passnumber": 1, "failnumber": 0, "notrunnumber": 0, "duration":00:11:03, "casenum":013}##
        ##sw.getCellValue of the row##
        casenum = dic_log['casenum']
        casename = sw.getCellValue(caselines[idx],2)
        casecmd = sw.getCellValue(caselines[idx],3)
        casetot = int(dic_log['failnumber'])+int(dic_log['passnumber']+int(dic_log['notrunnumber']))
        casepass = dic_log['passnumber']
        casefail = dic_log['failnumber']
        casetime = dic_log['duration']
        updateXML(filename=xmlfile, casename=casename, casenum=casenum, casecmd=casecmd,casetot=casetot,\
                  casepass=casepass,casefail=casefail,casetime=casetime)
        creatindexhtml(xmlfile,htmlfile)
    os.system('del ' + basedir + "\\log\\tmp.* " + r"/Q") #delete all tmp files
    uploadTestResult(logpath, uploadpath)
    os.system("xcopy /s " + filename + " " + "\"" + uploadpath + "\"")


def uploadTestResult(logpath, uploadpath):
    os.system("md "+"\""+uploadpath+"\"") #create stattime folder
    os.system("xcopy /s "+logpath+" "+"\""+uploadpath+"\"") #upload xml and logfile to starttime folder

def calduration(time1, time2):
    times = (time2-time1).seconds
    m, s = divmod(times, 60)
    h, m = divmod(m, 60)
    durtime = "%2d:%2d:%2d" % (h, m, s)
    return durtime


#def createReportXml(project, brand, sku, testjob,tpass, tfail, tnr, casename, casecmd, casenumber,casetotal,casepass,casefail):
def createReportXml(**kwargs):
    doc = Document()
    testreport = doc.createElement('testreport')
    doc.appendChild(testreport)
    testreportlist = kwargs
    for item in kwargs.keys():
        # Create brand node
        if(item=='filename'):
            continue
        cnode = doc.createElement(item)
        cnode_text = doc.createTextNode(str(kwargs[item]))
        cnode.appendChild(cnode_text)
        testreport.appendChild(cnode)
    with open(kwargs['filename'], 'w') as f:
        f.write(doc.toprettyxml(indent='\t'))
        f.close()
    return

def updateXML(**kwargs):
    doc = parse(kwargs['filename'])
    rootnode = doc.documentElement
    testcase = doc.createElement('testcase')
    rootnode.appendChild(testcase)
    for item in kwargs.keys():
        # Create brand node
        if(item=='filename'):
            continue
        cnode = doc.createElement(item)
        cnode_text = doc.createTextNode(str(kwargs[item]))
        cnode.appendChild(cnode_text)
        testcase.appendChild(cnode)
    with open(kwargs['filename'], 'w') as f:
        f.write(doc.toprettyxml(indent='\t'))
        f.close()
    return

def creatindexhtml(xmlfile,htmlfilename):
    with open(htmlfilename,"w", encoding='utf-8')as f:
    ##write html head
        head = """
    <html>
    <head>
    <title>Sanity Bluetooth_Firmware-v1.0</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">
    </head>
<body>
    <div>
            <table style="width:100%">
                <tbody>
                    <td style="width:19%; color:red">&emsp;&emsp;<b>Issues raised in this build iteration:</b>
                        <td style="width:71%">None</td>
                    <td style="width:10%">
                        <button type="submit" class="btn btn-warning" style="width:140px;font-size:15px;" data-toggle="modal" data-target="#myModal" name="jira_form" id="jira_form" onClick="myFunction()">Create JIRA issue</button>
                    </td>
                </tbody>
            </table>
    </div>
    <div class="container">
        <div class="row" id="head">
            <div class="col-xs-12">
            <h2 class="text-capitalize">Banneker Endpoint Test</h2>
    """
        f.write(head)
        #ET prase temp xml
        try:
            tree = et.parse(xmlfile)
            rootnode = tree.getroot()
        except Exception as e:
            raise("xml file not found!")
            sys.exit()
        for child in rootnode:
            if child.tag=="starttime":
                headstr = """<p class="attribute"><strong>Start Time:</strong>""" +child.text +"""</p> """
                f.write(headstr)
            if child.tag=="duration":
                headstr = """<p class="attribute"><strong>Duration: </strong>""" + child.text +"""</p> """
                f.write(headstr)
            if child.tag == "pass_count":
                passnum = int(child.text)
            if child.tag == "fail_count":
                failnum = int(child.text)
            if child.tag == "norun_count":
                notrun = int(child.text)
            if child.tag == "hw_version":
                headstr = """<p class="attribute"><strong>HW Version: </strong>""" + child.text +"""</p> """
                f.write(headstr)
            if child.tag == "sw_version":
                headstr = """<p class="attribute"><strong>SW Version: </strong>""" + child.text +"""</p> """
                f.write(headstr)
        headstr = """<p class="attribute"><strong>Summary: </strong>"""+"Total:"+str(passnum+failnum+notrun)+",Pass:"+str(passnum)+",Fail:"+str(failnum)+"""</p>
            </div>
        </div>"""
        f.write(headstr)
        #handle test case
        for testcase in rootnode.iter('testcase'):
            teststr="""<div class="row">
            <div class="col-xs-12 col-sm-10 col-md-10">
                <table class="table table-hover table-responsive">
                    <thead>
                        <tr>
                            <th>"""+testcase[0].text+"""</th><th>Status</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody>"""
            f.write(teststr)
            if int(testcase[5].text)>0:
                str1 = """ <tr class="warning">
                            <td class="col-xs-10">"""+testcase[2].text+""" </td><td class="col-xs-1">"""
                f.write(str1)
                f.write('''<span class="label label-warning" style="display:block;width:40px;">''')
                f.write("Error")
            else:
                str1 = """ <tr class="success">
                            <td class="col-xs-10">"""+testcase[2].text+""" </td><td class="col-xs-1">"""
                f.write(str1)
                f.write('''<span class="label label-success" style="display:block;width:40px;">''')
                f.write("Pass")
            teststr="""</span>
                            </td>
                            <td class="col-xs-1">
                                <button class="btn btn-default btn-xs"><a href="./case_"""+testcase[1].text+""".log">View</a></button>
                            </td>
                        </tr>
                        <tr style="display:none;">
                            <td class="col-xs-9" colspan="3"><p>hello world!</p></td>
                        </tr>
                        <tr>
                            <td colspan="3">"""+\
                                "Total:"+str(testcase[3].text)+", Pass: "+str(testcase[4].text)+", Error: "+str(testcase[5].text)+" -- Duration: "+testcase[6].text+""" s
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
            """
            f.write(teststr)
        #tail of html
        tailstr = """
            </div>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js"></script>
    <script type="text/javascript">
        $(document).ready(function(){
            $('td').on('click', '.btn', function(e){
                e.preventDefault();
                e.stopImmediatePropagation();
                var $this = $(this);
                var $nextRow = $this.closest('tr').next('tr');
                $nextRow.slideToggle("fast");
                $this.text(function(i, text){
                    if (text === 'View') {
                        return 'Hide';
                    } else {
                        return 'View';
                    };
                });
            });
        });
    </script>

</body></html>
        """
        f.write(tailstr)
        f.close()

if __name__ == '__main__':
    main()
