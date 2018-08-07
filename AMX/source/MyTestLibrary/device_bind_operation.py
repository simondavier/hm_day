#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os
from autoit import *

def open_bund():
    try:
        win_activate('[title:NetLinx Studio]')
    except ai.AutoItError:
        print('AutoItError happened, returned')
        return
    auto_it_set_option("MouseCoordMode", 2)
    send("!{SPACE}X")
    time.sleep(1)
    mouse_click("left",180,660)

def refresh_onlinetree():
    try:
        win_activate('[title:NetLinx Studio]')
    except ai.AutoItError:
        print('AutoItError happened, returned')
        return
    auto_it_set_option("MouseCoordMode", 2)
    control_click("[Title:NetLinx Studio]", 'Button12')
    time.sleep(1)
    mouse_click("left",320,100)
    time.sleep(3)

def deal_devicelist():
    sDut={}
    try:
        win_activate('[title:NetLinx Studio]')
    except ai.AutoItError:
        print('AutoItError happened, returned')
        return
    #control_tree_view("[title:NetLinx Studio]","SysTreeView322","Expand")
    iCount=control_tree_view("[title:NetLinx Studio]","SysTreeView322","GetItemCount")
    #print(iCount)
    for i in range(int(iCount)) :
        sText = control_tree_view("[title:NetLinx Studio]","SysTreeView322","GetText",extras1="#"+str(i),extras2="#0")
        sDut[sText]=i
    return sDut

def select_unbund_device(sDut):
    for device in sDut.keys():
        if "NDP Devices" in device:
            print(device)
            #bund device
            bond_device()
            refresh_onlinetree()
            
def bond_device():
    try:
        win_activate('[title:NetLinx Studio]')
    except ai.AutoItError:
        print('AutoItError happened, returned')
        return
    control_click("[Title:NetLinx Studio]", 'Button12')
    time.sleep(2)
    mouse_click("left",280,580)
    time.sleep(2)
    mouse_click("left",15,110)
    time.sleep(0.5)
    mouse_click("right",80,130)
    time.sleep(1)
    mouse_click("left",250,450)
    win_wait_active("[title:Bind/Unbind Device]", 3)
    mouse_click("left",370,323)
    time.sleep(0.5)
    control_click("[title:Bind/Unbind Device]", 'Button3')        
            
if __name__ == '__main__':
    #open_bund()
    refresh_onlinetree()
    #sDut = deal_devicelist()
    #print(sDut)
    #select_unbund_device(sDut)
    bond_device()