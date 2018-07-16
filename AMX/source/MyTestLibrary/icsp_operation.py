# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 15:38:25 2018

@author: WeicZhang
"""

import autoit as ai
import time
import logger

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
def get_comeback_message():
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