#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xml.dom.minidom import Document
FILENAME = "c:\\JenkinsTestReports\\workspace\\default.config"

class writetoreport:
    def __init__(self,duration, start_time, end_time, testcase_count, \
                     pass_count, fail_count, norun_count, hw_version, sw_version, phase):
        self.output = self.read_config_file(FILENAME)
        self.brand=self.output['brand']#'AMX'
        self.project=self.output['project']#'Banneker'
        self.sku=self.output['sku']#'endpoint_tx'
        self.testjob=self.output['testjob']#'video_control'
        self.duration=str(duration)#'00:11:03'
        self.start_time=str(start_time)#'2019-05-30_20-13-05'
        self.end_time=str(end_time)#'2019-06-02_00-02-33'
        self.testcase_count= str(testcase_count)#'2'
        self.pass_count=str(pass_count)#'2'
        self.fail_count=str(fail_count)#'0'
        self.norun_count=str(norun_count)#'0'
        self.tester=self.output['tester']#'HISNN834'
        self.hw_version=str(hw_version)#'V0.2'
        self.sw_version=str(sw_version)#'V1.0.1'
        self.phase=str(phase)#'EV'

    def read_config_file(self, filename):
        f = open(filename)
        a = f.readline()
        output={}
        while a:
            a = f.readline()
            if a.find('_Brand')!=-1:
                brand = a.split('=')[1].strip()
                output['brand']=brand
            elif a.find('_Project')!=-1:
                project = a.split('=')[1].strip()
                output['project']=project
            elif a.find('_Sku')!=-1:
                sku = a.split('=')[1].strip()
                output['sku']=sku
            elif a.find('_TestJob')!=-1:
                testjob = a.split('=')[1].strip()
                output['testjob']=testjob
            elif a.find('_Tester')!=-1:
                tester = a.split('=')[1].strip()
                output['tester']=tester
        f.close()
        if len(output)==5:
            return output
        else:
            raise RuntimeError('config file is not correct!')

    def writeInfoToXml(self, filename):
        doc = Document()
        testreport = doc.createElement('testreport')
        doc.appendChild(testreport)
        testreportlist = {'brand':self.brand, 'project':self.project,'sku':self.sku, 'testjob':self.testjob}
        for item in testreportlist:
        #Create brand node
            print(item)
            cnode = doc.createElement(item)
            print(testreportlist[item])
            cnode_text = doc.createTextNode(testreportlist[item])
            cnode.appendChild(cnode_text)
            testreport.appendChild(cnode)
        report = doc.createElement('report')
        testreport.appendChild(report)
        reportlist = {'duration':self.duration, 'start_time':self.start_time, 'end_time':self.end_time,'testcase_count':self.testcase_count, \
                      'pass_count':self.pass_count, 'fail_count':self.fail_count, 'norun_count': self.norun_count,'tester':self.tester, \
                      'hw_version':self.hw_version,'sw_version':self.sw_version, 'phase': self.phase}
        #Create duration node
        for ritem in reportlist:
            rnode = doc.createElement(ritem)
            rnode_text = doc.createTextNode(reportlist[ritem])
            rnode.appendChild(rnode_text)
            report.appendChild(rnode)
        # write dom to xml
        with open(filename, 'w') as f:
            #f.write(doc.toprettyxml(indent='\t', encoding='utf-8'))
            f.write(doc.toprettyxml(indent='\t'))
            f.close()
        return
# if __name__=='__main__':
#     writeobj = writetoreport('00:11:03','2019-05-30_20-13-05','2019-06-02_00-02-33',2,2,0,0,'V0.2','V1.0.1','EV')
#     writeobj.writeInfoToXml('beneker_rx_icsp_test20190814.xml')