# -*- coding: utf-8 -*-
"""
Created on Wed May 30 16:18:33 2018

@author: WeicZhang
"""

# -*- coding: utf-8 -*-
"""
Created on Tue May 29 17:52:40 2018

@author: WeicZhang
"""
# this function input is single command and output is the returned value
# if selected is zero, return value is ''
# if selected command is non-zero, return value is a list
import autoit as ai
import time
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
    time.sleep(2)
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
#%% test the function
#haha=command_thor_test('get status')        
#print(haha)