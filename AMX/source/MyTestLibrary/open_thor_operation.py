#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import os
from autoit import *
from icsp_operation import *
from telnet_operation import TelnetApp

#class openThorWindow(object):
class open_thor_operation(object):
    def __init__(self,devMac,sMac,username="administrator",pwd="password",sPort="1",sSystem="0"):
        self.devMac=devMac
        self.sMac=sMac
        self.username=username
        self.pwd=pwd
        self.sPort=sPort
        self.sSystem=sSystem    

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
        | open_thor_window | xx-xx-xx-xx-xx-xx,xx-xx-xx-xx-xx-xx,username,password,sPort,sSystem | 
        '''
        ip = self.open_netlinx()
        devIP = self.get_ip(self.devMac)
        tn = TelnetApp(ip,self.username,self.pwd)
        command = 'show device'
        out = tn.excut_command(command)
        print out
        dNumber, dName, dIP,dserial = tn.parse_get_device_and_ip(out)
        dic = {}
        for i in range(len(dNumber)):
            dic[dIP[i]] = dNumber[i]
        sDevice = self.devIp2port(dic, devIP)
        print ("the device ports is %s" % sDevice)
        self.open_notification(sDevice)
        time.sleep(2)
        send("!D")
        send("^C")
        win_wait_active("[title:Control a Device]", 3)
        time.sleep(0.5)
        control_set_text("[title:Control a Device]", "Edit1", sDevice)
        control_set_text("[title:Control a Device]", "Edit2", self.sPort)
        control_set_text("[title:Control a Device]", "Edit3", self.sSystem)
        tn.kill_connection()
    
    def open_netlinx(self):
        u'''
        open Netlinx and get the master ip from master Mac adress.
        @param:
        sMac: Master Mac address
        @return: 
        ip: master ip
        eg:
        | open_netlinx | xx-xx-xx-xx-xx-xx | 
        '''
        run("C:\Program Files (x86)\AMX Control Disc\NetLinx Studio 4\NSXV4.exe")
        win_wait_active("[Title:NetLinx Studio]", 3)
        send("!S")
        send("^W")
        send("!D")
        win_active("[Title:Communications Settings]")
        # clear All device
        time.sleep(5)
        control_click("[Title:Communications Settings]", "Button7")
        # Add a master to list
        send("!N")
        # sMac="00-60-9f-9d-90-03"
        ip = self.get_ip(self.sMac)
        time.sleep(1)
        win_wait_active("[title:New TCP/IP Setting]", 3)
        time.sleep(0.5)
        control_set_text("[title:New TCP/IP Setting]", "Edit1", ip)
        send("{ENTER}")
        time.sleep(0.5)
        send("{ENTER}")
        time.sleep(0.5)
        win_active("[Title:Workspace Communication Settings]")
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
        |open_notification|D, P, S | 
        '''
        self.sDevice=sDevice
        win_wait_active("[Title:NetLinx Studio]", 2)
        auto_it_set_option("MouseCoordMode", 2)
        mouse_click("left", 255, 14)
        time.sleep(0.5)
        mouse_click("left", 255, 25)
        time.sleep(0.5)
        win_wait_active("[title:NetLinx Device Notifications Options]", 5)
        time.sleep(0.5)
        control_click("[title:NetLinx Device Notifications Options]", 'Button5')
        time.sleep(0.5)
        control_click("[title:NetLinx Device Notifications Options]", 'Button2')
        time.sleep(0.5)
        win_wait_active("[title:NetLinx Notification Properties - [Add]]", 5)
        time.sleep(0.5)
        control_set_text("[title:NetLinx Notification Properties - [Add]]", "Edit1", self.sDevice)
        control_set_text("[title:NetLinx Notification Properties - [Add]]", "Edit2", self.sPort)
        control_set_text("[title:NetLinx Notification Properties - [Add]]", "Edit3", self.sSystem)
        control_click("[title:NetLinx Notification Properties - [Add]]", 'Button4')
        mouse_click("left", 40, 252)
        mouse_click("left", 40, 267)
        control_click("[title:NetLinx Notification Properties - [Add]]", 'Button7')
        time.sleep(0.5)
        win_active("[title:NetLinx Device Notifications Options]")
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
    
    # get ip from Macaddress
    def get_ip(self,sMac):
        u'''
        Using 'ARP -a' to query ip address according to MAC.
        @param:
        sMac: device MAC address
        @return:
        ip address
        eg:
        | get_ip | xx-xx-xx-xx-xx-xx |    
        '''
        self.sMac = sMac
        for line in os.popen("arp -a").readlines()[3:]:
            print line.split()[1]
            if (sMac in line.split()[1]):
                return line.split()[0]
        else:
            raise RuntimeError("No this MAC address found!!")
    
if __name__ == '__main__':
    
    devMac = "00-60-9f-a4-5f-ae"
    sMac = "00-60-9f-9d-90-03"
    otw = openThorWindow(devMac,sMac)
    otw.open_thor_win()  