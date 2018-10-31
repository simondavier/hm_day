#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import os
from os_cmd_operation import get_ip
from autoit import *
from icsp_operation import *
from device_bind_operation import *

#class openThorWindow(object):
class open_thor_operation(object):
    def __init__(self,devMac,sMac,username="administrator",pwd="password",sPort="1",sSystem="0"):
        self.devMac=devMac
        self.sMac=sMac
        self.username=username
        self.pwd=pwd
        self.sPort=sPort
        self.sSystem=sSystem
        self.sDeviceNum=None

    def open_thor_win(self):
        u'''
        Open thor command window to send command. the default user:administrator,pwd:password,Port:1, System:0
        @param:
        devMac: The DUT Mac address
        sMac: The Master Mac address
        user: user in telnet login
        pwd: password in telnet login
        sPort: The DUT port number
        sSystem: The DUT system number.
        eg:
        | open_thor_window |  | 
        '''
        try:
            win_activate('[title:NetLinx Studio]')
        except AutoItError:
            print('AutoItError happened, returned')
            return
        #ip = self.open_netlinx() #get master ip
        '''devIP = self.get_ip(self.devMac)
        tn = TelnetApp(ip,self.username,self.pwd)
        command = 'show device'
        out = tn.excut_command(command)
        print out
        dNumber, dName, dIP,dSerial = tn.parse_get_device_and_ip(out)
        dic = {}
        for i in range(len(dNumber)):
            dic[dIP[i]] = dNumber[i]
        sDevice = self.devIp2port(dic, devIP)
        sDevice = self.get_device_port(self.devMac)
        print ("the device ports is %s" % sDevice)
        self.sDeviceNum = sDevice
        self.open_notification(self.sDeviceNum)
        time.sleep(0.5)'''
        send("!D")
        time.sleep(0.5)
        send("+C")
        win_wait_active("[title:Control a Device]", 5)
        #if can not open "Control a Device" window, then reclick it again
        #if(ret==0):
        time.sleep(2)
        mouse_click("left",255,14)
        time.sleep(2)
        mouse_click("left",255,180)
        time.sleep(0.5)
        control_set_text("[title:Control a Device]", "Edit1", self.sDeviceNum)
        control_set_text("[title:Control a Device]", "Edit2", self.sPort)
        control_set_text("[title:Control a Device]", "Edit3", self.sSystem)
        #tn.kill_connection()
    
    def open_netlinx(self):
        u'''
        open Netlinx and get the master ip from master Mac adress.
        @param:
        sMac: Master Mac address
        @return: 
        ip: master ip
        eg:
        | open_netlinx | | 
        '''
        run("C:\Program Files (x86)\AMX Control Disc\NetLinx Studio 4\NSXV4.exe")
        win_wait_active("[Title:NetLinx Studio]", 3)
        send("!S")
        time.sleep(0.5)
        send("+W")
        time.sleep(0.5)
        send("!D")
        win_wait_active("[Title:Communications Settings]",10)
        # clear All device
        control_click("[Title:Communications Settings]", "Button7")
        # Add a master to list
        send("!N")
        # sMac="00-60-9f-9d-90-03"
        ip = get_ip(self.sMac)#get master ip via Mac address
        time.sleep(1)
        win_wait_active("[title:New TCP/IP Setting]", 3)
        time.sleep(0.5)
        control_set_text("[title:New TCP/IP Setting]", "Edit1", ip)
        send("{ENTER}")
        time.sleep(0.5)
        send("{ENTER}")
        time.sleep(0.5)
        win_wait_active("[Title:Workspace Communication Settings]", 3)
        time.sleep(0.5)
        control_click("[Title:Workspace Communication Settings]", 'Button2')
        return ip
    
    def open_notification(self,sDevice):
        u'''
        open notification and config notification window with D.P.S
        @param:
        sDevice: The DUT device
        sPort: The DUT port
        sSystem: The DUT under system
        eg:
        |open_notification|Device "D" | 
        '''
        win_active("[Title:NetLinx Studio]")
        auto_it_set_option("MouseCoordMode", 2)
        time.sleep(0.5)
        #send("!D")
        mouse_click("left",255,14)
        time.sleep(0.5)
        mouse_click("left",255,25)
        #send("+O")
        win_wait_active("[title:NetLinx Device Notifications Options]", 5)
        time.sleep(0.5)
        control_click("[title:NetLinx Device Notifications Options]", 'Button5')
        time.sleep(0.5)
        control_click("[title:NetLinx Device Notifications Options]", 'Button2')
        time.sleep(0.5)
        win_wait_active("[title:NetLinx Notification Properties - [Add]]", 5)
        time.sleep(0.5)
        control_set_text("[title:NetLinx Notification Properties - [Add]]", "Edit1", sDevice)
        control_set_text("[title:NetLinx Notification Properties - [Add]]", "Edit2", self.sPort)
        control_set_text("[title:NetLinx Notification Properties - [Add]]", "Edit3", self.sSystem)
        control_click("[title:NetLinx Notification Properties - [Add]]", 'Button4')
        mouse_click("left", 40, 252)
        mouse_click("left", 40, 267)
        control_click("[title:NetLinx Notification Properties - [Add]]", 'Button7')
        time.sleep(0.5)
        win_wait_active("[title:NetLinx Device Notifications Options]",3)
        time.sleep(0.5)
        control_click("[title:NetLinx Device Notifications Options]", 'Button6')
        time.sleep(1)
        send("!D")
        send("^N")
    
    # get the device id
    def devName2port(self,dic, devName):
        u'''
        find device port from devName
        @param:
        dic: dictionary of devicename, deviceport
        @return: 
        port: device port
        eg:
        | devName2port | dic, deviceName| 
        '''
        self.dic = dic
        self.devName = devName
        if(dic.has_key(devName)):
            return dic[devName]
        else:
            raise RuntimeError("can not find the device under current master!!")
    
    def devIp2port(self,dic, devIP):
        u'''
        find device port from devIp
        @param:
        dic: dictionary of devicename, deviceport
        @return: 
        port: device port
        eg:
        | devIp2port | dic, deviceName|
        '''
        self.dic= dic
        self.devIP = devIP
        if(dic.has_key(devIP)):
            return dic[devIP]
        else:
            raise RuntimeError("can not find the device under current master!!")

    #close Netlinx Studio
    def close_thor_operation(self):
        u'''
        close thor command window
        '''
        win_wait_active("[title:Control a Device]",3)
        #close thor window
        send("!{F4}")
        time.sleep(0.5)
        win_active("[title:NetLinx Studio]")
        send("!F")
        time.sleep(0.5)
        send("+x")
    
    '''def __del__(self):
        class_name=self.__class__.__name__
        print("object has been delete") 
     '''          
    def get_device_ip(self,sMac):
        u'''
        Get device ip address from csv report.
        @param: DUT Mac address
        @return: device ip address
        eg:
        | get_device_ip | xx-xx-xx-xx-xx-xx |
        '''
        user = os.path.expanduser('~')
        temp_path=user+"\AppData\Local\Temp\OnlineTreeReport.csv"
        csv_reader = csv.reader(open(temp_path, 'r'))
        sMac=sMac.replace("-",":")
        for row in csv_reader:
            if sMac in row:
                return row[6]
        else:
            raise RuntimeError("ip address can not be found with this MacAddress!")
    
    def get_device_port(self,sMac):
        u'''
        Get device "D"  from csv report.
        @param: DUT Mac address
        @return: device ip address
        eg:
        | get_device_ip | xx-xx-xx-xx-xx-xx |
        '''
        user = os.path.expanduser('~')
        temp_path=user+"\AppData\Local\Temp\OnlineTreeReport.csv"
        csv_reader = csv.reader(open(temp_path, 'r'))
        sMac=sMac.replace("-",":")
        for row in csv_reader:
            if sMac in row:
                if row[0]!="0":
                    self.sDeviceNum=row[0]
                    return row[0]
                else:
                    raise RuntimeError("This device can not be found in CSV")
        else:
            raise RuntimeError("No this MacAddress Found in CSV!")
    
if __name__ == '__main__':
    
    devMac = "00:60:9f:a4:5f:ae"
    sMac = "00-60-9f-9d-8f-55"
    otw = open_thor_operation(devMac,sMac)
    ip_ms = otw.open_netlinx()
    #TODO:refresh online tree,bind device,Create CSV
    click_onlinetree_tab()
    refresh_onlinetree()
    while True:
        sDut = check_ubund()
        if sDut:
            bind_device()
        else:
            print 'no device need bind'
            break
    creat_online_tree_report()
    #TODO get device port from csv and device's ip
    print otw.get_device_ip(devMac)
    sDeviceNum = otw.get_device_port(devMac)
    #TODO open_notification
    otw.open_notification(sDeviceNum)
    #TODO open_thor_win
    otw.open_thor_win()
    
    
   