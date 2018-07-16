# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 20:30:20 2018

@author: WeicZhang
"""

from Telnet_SSH.telnet_library_for_RF import *

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
    
    