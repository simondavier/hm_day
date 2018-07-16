# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 09:29:12 2018
folder is  D:\projects\AMX\SW2106_NX-x200_Device_v1_1_42
@author: WeicZhang
"""

from autoit import *
import time

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
    
   