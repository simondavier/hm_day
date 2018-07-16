# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 09:29:12 2018
#device is the device number
system is system number
you should know the device and system number 
the mechanism is mouse click the relative position and load the given folder name
if device or system numebr is not correct, will raise the info 'Setting the Device Address Information was NOT successful'

@author: WeicZhang
"""

from autoit import *
import time

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
    
    
    
#    print('reset facotry by ns is done')
#    win_wait_active("[title:Select Folder]",5)
#    control_set_text("[title:Select Folder]","Edit1",folder)
#    time.sleep(.500)
#    control_click("[title:Select Folder]","Button1")
#    time.sleep(.500)
#    win_activate("[title:Send to NetLinx Device]")
#    mouse_click("left",60,153)
#    time.sleep(.500)
#    control_click("[title:Send to NetLinx Device]","Button7")