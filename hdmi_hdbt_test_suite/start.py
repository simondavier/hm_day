#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
from datetime import datetime
from json import loads
import switchconfig_operation as switchconfig
import write2dashboard

passnumber = 0
failnumber = 0

def main():
    global  passnumber, failnumber
    #select case;
    #basedir = (os.path.dirname(os.path.abspath(__file__)))
    basedir = "C:\\Simon\\CrickTest"
    filename = basedir+"\\TestCaseManagement.xlsx"
    sw= switchconfig.SwitchConfigOperation(filename, 0)
    result = sw.getSupportTimingCode(4)

    #handle history logfile, first copy , then delete
    os.system('del ' + basedir + "\\Report.xml " + r"/Q")
    os.system('del '+basedir +"\\log "+r"/Q")
    #run case;
    starttime = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
    time1 = datetime.now()
    for i in result:
        print(i)
        os.system(basedir+"\\"+i)
    endtime = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
    time2 = datetime.now()
    duration = calduration(time1, time2)
    #get the case result;
    tmplog = basedir+"\\log\\"+"tmp.log"
    for line in open(tmplog, 'r'):
        #print(line)
        dicres = loads(line)
        if dicres['failnumber'] >= 1:
            failnumber+=1
        else:
            passnumber+=1
    #create report
    totalnumber = sw.getRowsLenth()-1
    notrunnumber = totalnumber-passnumber-failnumber
    hwversion = "V0.3"
    swversion = "R4"
    phase = "DV"
    writeobj = write2dashboard.writetoreport(duration, starttime, endtime, totalnumber, passnumber, failnumber, notrunnumber, hwversion, swversion, phase)
    xmlpath = basedir+"\\log\\Report.xml"
    writeobj.writeInfoToXml(xmlpath)
    project = writeobj.output['project']
    sku = writeobj.output['sku']
    testjob = writeobj.output['testjob']
    logpath = basedir+"\\log"
    uploadpath = "C:\\JenkinsTestReports\\workspace\\"+project+"\\"+sku+"\\"+testjob+"\\"+starttime
    uploadTestResult(logpath, uploadpath)

def uploadTestResult(logpath, uploadpath):
    os.system("md "+"\""+uploadpath+"\"") #create stattime folder
    os.system("xcopy /s "+logpath+" "+"\""+uploadpath+"\"") #upload xml and logfile to starttime folder

def calduration(time1, time2):
    times = (time2-time1).seconds
    m, s = divmod(times, 60)
    h, m = divmod(m, 60)
    durtime = "%2d:%2d:%2d" % (h, m, s)
    return durtime

if __name__ == '__main__':
    main()
