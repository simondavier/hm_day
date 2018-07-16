# -*- coding: utf-8 -*-

import autoit as ai
import time

def getChn(deviceID):
    chnList1=[]
    chnList2=[]
    chnList3=[]
    chnList4=[]
    chnList5=[]
    chnList6=[]
    chnList7=[]
    chnList8=[]
    outputList=[]
    
    ai.win_activate('[title:NetLinx Studio]')   #active NetLinx Studio
    time.sleep(0.1)
    ai.opt("MouseCoordMode", 2)
    ai.mouse_click("left",260,14)
    time.sleep(0.1)
    ai.mouse_click("left",260,180)
    time.sleep(0.1)
        
    for chnID in range(1,9):
        command_input="?OUTPUT-ALL," + str(chnID)
        
        ai.win_activate('[title:Control a Device]')   #active "control a device" window
        time.sleep(0.1)
        ai.control_focus('[title:Control a Device]','Edit8')  #get focus to command input text field
        time.sleep(0.1)
        ai.control_set_text('[title:Control a Device]', 'Edit1', deviceID)  #set Device ID
        time.sleep(0.1)
        ai.control_set_text('[title:Control a Device]','Edit8',command_input)  #input command
        time.sleep(1)
        ai.control_click('[title:Control a Device]','Button15')  #clear the command window
        time.sleep(0.5)
        ai.control_click('[title:Control a Device]','Button13')  # click "send to device" button 
        time.sleep(2)
        ai.win_activate('[title:NetLinx Studio]')
        time.sleep(1)
        ai.control_list_view('[title:NetLinx Studio]','SysListView325','SelectAll')  #SysListView325 or 328
        haha=ai.control_list_view('[title:NetLinx Studio]','SysListView325','GetSelectedCount')
        selected=int(haha)

        out=''
        for i in range(0,selected):
            out=out+ai.control_list_view('[title:NetLinx Studio]','SysListView325','GetText',extras1=str(i),extras2='0')

        outString=list(out)
        newStr=outString[out.find("SWITCH",0,len(outString)):]
        
        inChn=0
        outChn=0
        
        if newStr[-4].isdigit():
            inChn=int(newStr[-8])  #get input channel number
            outChn=int(newStr[-4])  #get output channel number  
        else:
            inChn=int(newStr[-6]) 
            outChn=0
            
        eval("chnList" + str(chnID)).append(outChn)
        eval("chnList" + str(chnID)).append(inChn)
                       
        outputList.append(eval("chnList" + str(chnID)))
    
    return outputList

print getChn("5008")
