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
import re
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
	for i in range(1,arg+1):
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
        #print('try '+str(count)+' time')
        out = get_comeback_message()
        if out!='':
            #print('congratulations! the output is not empty')
            break
        elif count<=3:
            time.sleep(3)
        else:
            #print('even tried 4 times, the output is still empty')
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
       
def factory_matrix():
    u'''
    set device to '0'
    | factory_matrix |
    '''
    #reset device
    command = 'CI0OALL'
    command_thor_test(command)

def random_switch(input,output,times):
    u'''
    random switch the input and output
    @param:
    input: input num
    output: output num
    times:  run times
    @return: a boolean 
    '''
    #init test device
    factory_matrix()
    matrix =  get_matrix(input, output+2)
    for i in range(times):
        sInput = str(random.randint(1,input))
        sOutput = generate_random_port(output)
        list=sOutput.split(',')
        #reset device
        factory_matrix()
        #get current matrix
        matrix =  get_matrix(input, output+2)
        set_matrix(matrix,sInput, sOutput)
        print 'after set, the matrix is:'
        print matrix
        #send command to device
        command='CI'+sInput+'O'+sOutput
        print 'send command is:'+command
        command_thor_test(command)
        newMatrix = get_matrix(input,output+2)
        print newMatrix
        if(len(list)<output):
            if(compare_matrix(matrix, newMatrix)):
                continue
            else:
                print 'Input:'+sInput+'Output:'+sOutput
                return False
        else:
            print 'all port'
            matrix[int(sInput)-1][output]=1
            print matrix
            if(compare_matrix(matrix, newMatrix)):
                continue
            else:
                print 'Input:'+sInput+'to all failed'
                return False
    return True

def order_swtich(input,output):
    u'''
    @param: 
    input: input port
    output: output port
    @return: Boolean
    Ordered switch the input to output port 
    '''
    #start order switch
    for iInput in range(1,input+1):
        #reset device
        factory_matrix()
        #get current matrix
        matrix = get_matrix(input, output+2)
        for iOutput in range(1,output+1):
            in_id = str(iInput)
            ou_id = str(iOutput)
            print 'begin set:'
            set_matrix(matrix, in_id, ou_id)
            print 'print origin after modified'
            print matrix
            command='CI'+in_id+'O'+ou_id
            command_thor_test(command)
            newMatrix = get_matrix(input,output+2)
            print 'the newMatrix after set is: '
            print newMatrix
            if(iOutput<output):
                print 'not all port'
                if(compare_matrix(matrix, newMatrix)):
                    continue
                else:
                    print 'Input:'+in_id+'Output:'+ou_id
                    return False
            else:
                print 'all port'
                matrix[iInput-1][output]=1
                print matrix
                if(compare_matrix(matrix, newMatrix)):
                    continue
                else:
                    print 'Input:'+in_id+'Output:'+ou_id
                    return False
    
    #order to all port
    for i in range(input+1):
        #reset matrix
        factory_matrix()
        matrix = get_matrix(input, output+2)
        #Start to all port
        sInput=str(i)
        set_matrix(matrix, sInput, 'ALL')
        command = 'CI'+sInput+'OALL'
        command_thor_test(command)
        newMatrix = get_matrix(input,output+2)
        if(compare_matrix(matrix, newMatrix)):
            continue
        else:
            print 'Input:'+sInput+'To ALL'
            return False                
    return True                  
              
def compare_matrix(srcM,dstM):
    u'''
    @param src_Matrix, dstMatrix
    @return boolean, equal is True
    eg:
    | compare_matrix | srcMatrix | dstMatrix |
    '''
    s_irow=len(srcM)
    s_icolumn=len(srcM[0])
    d_irow=len(dstM)
    d_icolumn=len(dstM[0])
    if(s_irow!=d_irow or s_icolumn!=d_icolumn):
        return False
    for i in range(s_irow):
        for j in range(s_icolumn):
            if(srcM[i][j]!=dstM[i][j]):
                return False
    else:
        return True

def set_matrix(matrix,input,output):
    u'''
    @param:
    matrix: origin matrix;
    sInput: set input port;
    sOutput: set output port:
    @return: matrix after set
    eg:
    | set_matrix | matrix | input | output |
    '''
    if input == '0' and output == 'ALL':
        return reset_matrix(matrix)
    elif output == 'ALL':
        for i in range(len(matrix[0])):
            matrix[int(input)-1][i]=1
        return matrix
    else:
        outlist=output.split(',')
        for str in outlist:
            matrix[int(input)-1][int(str)-1]=1
        return matrix    

def reset_matrix(matrix):
    u'''
    @param: matrix
    @return: reset matrix  
    reset the matrix to 0
    | reset_matrix | matrix |
    '''
    iRow=len(matrix)
    iColumn=len(matrix[0])
    for i in range(iRow):
        for j in range(iColumn):
            if matrix[i][j]!=0:
                matrix[i][j]=0
    return matrix

def get_matrix(iInput,iOutput):
    u'''
    @param: 
    int input: input port
    int output:  output port + all port
    @return: matrix
    For example:
    EXP-MX-0808, input should be 8, output should be 10 (output has addtional status:none and all).eg:
    | get_matrix | input | output|
    '''
    #define and init a matrix with default 0
    matrix = [[0 for i in range(iOutput-1)] for i in range(iInput)]
    #Check input of all output
    for input_id in range(1,iInput+1):
        command="?INPUT-ALL," + str(input_id)
        out = command_thor_test(command)
        #abstract output number to list
        outlist = ''.join(re.findall('\( (.*?)\)',out)).split()
        #if it is no output?
        if len(outlist)==0:
            print "no output"
            continue
        #if it is all output?if yes, set all "1"
        elif len(outlist)==(iOutput-2):
            print "all output"
            for i in range(0,iOutput-1):
                matrix[input_id-1][i]=1
        #if it is some output?if yes, set to "1"
        else:
            print "some output"
            for output_id in outlist:
                matrix[input_id-1][int(output_id)-1]=1
    return matrix       