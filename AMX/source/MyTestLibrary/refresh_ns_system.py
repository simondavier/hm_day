# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 09:08:43 2018

@author: WeicZhang
"""

import autoit as ai
import time

def ns_refresh_system():
   # ai.win_activate("[CLASS:Afx:00D80000:8:00010003:00000000:014702D7]")
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
