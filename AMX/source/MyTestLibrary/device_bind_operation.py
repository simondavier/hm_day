#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os
import csv
from autoit import *
global windowsize
windowsize=[0,0]
def click_onlinetree_tab():
    u'''
    Maximize Netlinux Studio, and switch to onlinetree tab
    '''
    global windowsize
    try:
        win_activate('[title:NetLinx Studio]')
    except AutoItError:
        print('AutoItError happened, returned')
        return
    auto_it_set_option("MouseCoordMode", 2)
 
    send("!{SPACE}X")
    winsize = win_get_client_size('[title:NetLinx Studio]')
    windowsize[0]=winsize[0]
    windowsize[1]=winsize[1]
    x = windowsize[0]
    y = windowsize[1]
    time.sleep(1)
    mouse_click("left",180,y-38)#38 is pixels related to bottom of NS window

def refresh_onlinetree():
    u'''
    Refresh the online tree view, 5 seconds wait after refresh done.
    '''
    try:
        win_activate('[title:NetLinx Studio]')
    except AutoItError:
        print('AutoItError happened, returned')
        return
    auto_it_set_option("MouseCoordMode", 2)
    
    x = windowsize[0]
    y = windowsize[1]
    control_click("[Title:NetLinx Studio]", 'Button12')
    time.sleep(1)
    mouse_click("left",320,y-600)
    time.sleep(5)

def deal_devicelist():
    u'''
    To deal with the tree view the first items, and return a dic for the first DUT
    @return: 
    '''
    sDut={}
    try:
        win_activate('[title:NetLinx Studio]')
    except AutoItError:
        print('AutoItError happened, returned')
        return
    #control_tree_view("[title:NetLinx Studio]","SysTreeView322","Expand")
    iCount=control_tree_view("[title:NetLinx Studio]","SysTreeView322","GetItemCount")
    #print(iCount)
    for i in range(int(iCount)) :
        sText = control_tree_view("[title:NetLinx Studio]","SysTreeView322","GetText",extras1="#"+str(i),extras2="#0")
        sDut[sText]=i
    return sDut

def click_collapse_tree():
    u'''
    To cllapse the online tree list
    '''
    try:
        win_activate('[title:NetLinx Studio]')
    except AutoItError:
        print('AutoItError happened, returned')
        return
    control_click("[Title:NetLinx Studio]", 'Button12')
    auto_it_set_option("MouseCoordMode", 2)    
    x = windowsize[0]
    y = windowsize[1]
    
    time.sleep(1)
    mouse_click("left",320,y-125)
    time.sleep(1)
def click_to_expand_unbund_devices():
    u'''
    To expand the unbund device, and click "+" of unbund device
    '''
    try:
        win_activate('[title:NetLinx Studio]')
    except AutoItError:
        print('AutoItError happened, returned')
        return
    
    auto_it_set_option("MouseCoordMode", 2)    
    time.sleep(1)
    mouse_click("left",19,110)#click the "+" icon    
    
def rightclick_unbund_device():
    u'''
    Right click on Unbund device, select "Network Bind/Unbind Devices"
    '''
    try:
        win_activate('[title:NetLinx Studio]')
    except AutoItError:
        print('AutoItError happened, returned')
        return
    
    auto_it_set_option("MouseCoordMode", 2)    
    time.sleep(1)
    mouse_click("right",130,125)
    time.sleep(1)
    mouse_click('left',234,439)
    time.sleep(3)
           
def click_bond_device():
    u'''
    Wait Bind/unbind Device window, and check unbund device to bind
    '''
    win_activate("[title:Bind/Unbind Device]")
    time.sleep(1)
    mouse_click("left",40,110)
    time.sleep(0.5)
    control_click("[title:Bind/Unbind Device]", 'Button3')
    print 'waiting for device binding.... about 20seconds '
    time.sleep(20)
    refresh_onlinetree()

def check_ubund():
    u'''
    To check if the online tree has unbind device.
    @return: 
    True:  unbind device exists
    False: no unbond device
    '''
    try:
        win_activate('[title:NetLinx Studio]')
    except AutoItError:
        print('AutoItError happened, returned')
        return
    #get tree list #0 device
    iCount=control_tree_view("[title:NetLinx Studio]","SysTreeView322","GetItemCount")
    print iCount
    for i in range(int(iCount)) :
        sText = control_tree_view("[title:NetLinx Studio]","SysTreeView322","GetText",extras1="#"+str(i),extras2="#0")
        if sText.find('Unbound NDP Devices')>=0 or \
           sText.find('Searching NDP Devices')>=0 :
            return True
    else:
        print ("no unbind device")
        return False
    
def bind_device():
    u'''
    Process to bond device
    '''
    refresh_onlinetree()
    click_collapse_tree()
    click_to_expand_unbund_devices()
    rightclick_unbund_device()
    click_bond_device()
                
def creat_online_tree_report():
    u'''
    To creat online tree report(.csv)
    '''
    try:
        win_activate('[title:NetLinx Studio]')
    except AutoItError:
        print('AutoItError happened, returned')
        return
    auto_it_set_option("MouseCoordMode", 2)
    
    x = windowsize[0]
    y = windowsize[1]
    control_click("[Title:NetLinx Studio]", 'Button12')
    time.sleep(1)
    mouse_click("left",320,y-400)
    time.sleep(1)
    win_activate("[title:Online Tree Report]")
    control_click("[title:Online Tree Report]", 'Button6')
    time.sleep(5)
    send("!{F4}")

def check_online_report(sMac):
    u'''
    Check the online tree report according to Device Mac address, if return >0,
    that means device bind successful. 
    '''
    #sMac="00:60:9f:a4:5f:16"
    sMac = sMac.replace("-",":")
    user = os.path.expanduser('~')
    temp_path=user+"\AppData\Local\Temp\OnlineTreeReport.csv"
    csv_reader = csv.reader(open(temp_path, 'r'))
    for row in csv_reader:
        if sMac in row:
            return row[0]
    else:
        return 1

             
'''if __name__ == '__main__':
    sMac="00-60-9f-a4-5f-16"
    click_onlinetree_tab()
    while True:
        sDut = check_ubund()
        if sDut:
            bind_device()
        else:
            print 'no device need bind'
            break
    creat_online_tree_report()
    res=check_online_report(sMac)
    print res
'''    
    