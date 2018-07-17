#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on Jun 28, 2018
@author: WeiCai Simon
'''
#import library
import logger
import random
from autoit import *
import autoit as ai
import time
import Tkinter
#import Tkinter.messagebox
#from Telnet_SSH.telnet_library_for_RF import *
logger.initLogger()

#init RobotFramework
ROBOT_LIBRARY_SCOPE = "GLOBAL"
ROBOT_EXIT_ON_FAILURE = True

def generate_random_port(arg):
	u'''
	input: max of random port number
    output: random number str of port	
	use to generate random list.  eg:
	| generate | arg |
	'''
	arg = int(arg)
	list = []
	listsample = []
	list_res=[]
	for i in range(1,arg):
		list.append(i)
	step = random.randint(1,arg)
	if step<arg:
		listsample = random.sample(list,step)
		listsample.sort()
		list_res=map(str,listsample)
		str1 = ','.join(list_res)
		return str1
	else:
		list_res=map(str,list)
		str2 = ','.join(list_res)
		return str2

def get_comeback_message():
    ai.control_list_view('[title:NetLinx Studio]','SysListView328','SelectAll')
    haha=ai.control_list_view('[title:NetLinx Studio]','SysListView328','GetSelectedCount')
    selected=int(haha)
    
    if selected==0:
        out=''
    else:
        out=''
        
        for i in range(0,selected):
            out=out+ai.control_list_view('[title:NetLinx Studio]','SysListView328','GetText',extras1=str(i),extras2='0')
        
    return out


def command_thor_test(command):
    try:
        ai.win_activate('[title:Control a Device]')
    except ai.AutoItError:
        print('AutoItError happened, returned')
        return
    time.sleep(0.1)
    ai.control_focus('[title:Control a Device]','Edit8')
    time.sleep(0.1)
    ai.control_set_text('[title:Control a Device]','Edit8',command)
    time.sleep(1)
    ai.control_click('[title:Control a Device]','Button15')  #clear the command window
    time.sleep(0.5)
    ai.control_click('[title:Control a Device]','Button13')  #send the command work
    time.sleep(4)
    ai.win_activate('[title:NetLinx Studio]')
    time.sleep(1)
    count = 0
    while True:
        count+=1
        print('try '+str(count)+' time')
        out = get_comeback_message()
        if out!='':
            print('congratulations! the output is not empty')
            break
        elif count<=3:
            time.sleep(3)
        else:
            print('even tried 4 times, the output is still empty')
            break
    return out	

logger.cfgLevel("debug")
def click_ClearList():
    try:
        ai.win_activate('[title:ICSPMonitor - V7.2.115]')
    except ai.AutoItError:
        #print('AutoItError happened, returned')
        logger.prt.debug('AutoItError happened,could not detect ICSPMonitor Window, returned')
        return
    time.sleep(0.1)
    ai.control_click('[title:ICSPMonitor - V7.2.115]','Button4')
	
"""def get_comeback_message():
    ai.control_list_view('[title:ICSPMonitor - V7.2.115]','SysListView321','SelectAll')
    haha=ai.control_list_view('[title:ICSPMonitor - V7.2.115]','SysListView321','GetSelectedCount')
    selected=int(haha)
    
    if selected==0:
        out=''
    else:
        out=''
        
        for i in range(0,selected):
            out=out+'\n'+ai.control_list_view('[title:ICSPMonitor - V7.2.115]','SysListView321','GetText',extras1=str(i),extras2='0')
        
    return out   
"""

def ns_refresh_system():
    #ai.win_activate("[CLASS:Afx:00D80000:8:00010003:00000000:014702D7]")
    #ai.win_activate('[CLASSNAMENN:SysTreeView322]')
    try:
        ai.win_activate('[title:NetLinx Studio]')
    except ai.AutoItError:
        print('AutoItError happened, returned')
        return
    #ai.control_focus('[title:NetLinx Studio]','SysTreeView322')
    
    ai.opt("MouseCoordMode",2)
    ai.mouse_click("right",20,200)
    time.sleep(0.5)
    ai.mouse_click("left",40,130)
    print('refresh sucess')

def reset_factory_by_ns(device,system):
    device = str(device)
    system = str(system)
    win_activate("[title:NetLinx Studio]")
    opt("MouseCoordMode", 2) ;
    
    mouse_click("left",260,14)#click Diagnostics
    time.sleep(0.500)
    
    mouse_click("left",260,220)#click device addressing
    time.sleep(.500)
#    mouse_click("left",650,50)
    win_wait_active("[title:Device Addressing]",5) #wait for window device addressing appear
    control_set_text("[title:Device Addressing]","Edit1",device)#input device number in edit1
    time.sleep(.5)
    control_set_text("[title:Device Addressing]","Edit3",system)#input system number in edit3
    time.sleep(.5)
    control_click("[title:Device Addressing]","Button7")#click button reset factory
    time.sleep(.5)
    try:
        win_wait_active("[title:NetLinx Studio]",2)
        time.sleep(.5)
        control_click("[title:NetLinx Studio]",'Button1')
        time.sleep(.5)
        control_click("[title:Device Addressing]","Button11")
        raise Exception('Setting the Device Address Information was NOT successful')
    except Exception :
        print('Setting the Device Address Information was NOT successful')
    except:
        control_click("[title:Device Addressing]","Button11")
        print('reset facotry by ns is done')

def show_message_box():
    root = tkinter.Tk()
    tkinter.messagebox.showinfo('notice','please push reset button  at least 10 seconds!')
    root.destroy()


def update_fw_by_ns(folder,device=0,system=1):
    #folder is the firmware location string
    #the mechanism is mouse click the relative position and load the given folder name
    device = str(device)
    system = str(system)
    win_activate("[title:NetLinx Studio]")
    opt("MouseCoordMode", 2) 
    
    mouse_click("left",361,14)
    time.sleep(0.500)
    
    mouse_click("left",363,50)
    time.sleep(.500)
    mouse_click("left",650,50)
    win_wait_active("[title:Send to NetLinx Device]",5)
    control_click("[title:Send to NetLinx Device]","Button2")
    win_wait_active("[title:Select Folder]",5)
    control_set_text("[title:Select Folder]","Edit1",folder)
    time.sleep(.500)
    control_click("[title:Select Folder]","Button1")
    time.sleep(.500)
    win_activate("[title:Send to NetLinx Device]")
    mouse_click("left",60,153) #select the first kit file in the folder
    time.sleep(.500)
    control_set_text("[title:Send to NetLinx Device]","Edit1",device)#input device number in edit1
    time.sleep(.5)
    control_set_text("[title:Send to NetLinx Device]","Edit3",system)#input system number in edit3
    time.sleep(.5)
    control_click("[title:Send to NetLinx Device]","Button9") #select legacy icsp firmware transfer
    time.sleep(.5)
    control_click("[title:Send to NetLinx Device]","Button7")# click the send button
    while True:
        time.sleep(30)
        text = control_get_text("[title:Send to NetLinx Device]","Button8")
        if text=='Cancel':
            print('upgrading is ongoing!')
        else:
            print('upgrading done!')
            control_click("[title:Send to NetLinx Device]","Button8")#click the finish button, if not finish, this will couse cancel upgrade
            break

def usb_fw_update(ip,username,pwd,device):
    device = str(device)# if device is 0, update master firmware, if device is 5001, upgrade device fw
    tn = build_connection(ip,username,pwd)
    if type(tn)==telnetlib.Telnet:
        out1 = excut_command(tn,'import kit')
        if 'Select device' in out1:
            out2 = excut_command(tn,device)
            if 'Select kit by number' in out2:
                out3 = excut_command(tn,'1')# always select number1 so you should put only one kit file in usb drive
                if 'Extracting kit file' in out3:
                    time.sleep(120) # 
                    print('update success,please notice the led indicate normal status')
                else:
                    print('update failed')
                
            else:
                print('something wrong in select kit file')
        else:
            print('something wrong in select device') 
        kill_connection(tn)
    else:
        print('telnet is not connected')
        return			