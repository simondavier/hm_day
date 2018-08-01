#!/usr/bin/env python
# -*- coding: utf-8 -*-

from icsp_operation import *
from open_thor_operation import open_thor_operation
import logger

logger.initLogger()

#init RobotFramework
ROBOT_LIBRARY_SCOPE = "GLOBAL"
ROBOT_EXIT_ON_FAILURE = True

devMac = "00-60-9f-a4-5f-ae"
#devMac = "xx-xx-xx-xx-xx-xx"
sMac = "00-60-9f-a4-0e-a9"
#sMac = "xx-xx-xx-xx-xx-xx"
username="administrator"
pwd="password"
sPort = "1"
sSystem = "0"

def open_thor_command(sDmac="",sMMac="",sUsername="",sPwd="",sP="",sSys=""):
    u'''
    if you want to test icsp command from NetlinxStudio, this config will
    open Netlinux Studio and thor command windows automatic.
    @param:
    sDmac(required): Device Mac address, default"xx-xx-xx-xx-xx-xx"
    sMMac(required): Master Mac address, default"xx-xx-xx-xx-xx-xx"
    username: the username of master telnet username, default:"administrator"
    pwd: the password of master telnet password, default:"password"
    sPort: P port of the master, default: "1"
    sSystem: S port of the master, default: "0"
    eg:
    | open_thor_command | sDmac,sMMac,<sUsername>,<sPwd>,<sP>,<sSys> |
    '''
    global devMac,sMac,username, pwd, sPort, sSystem
    if sDmac == "": sDmac = devMac
    if sMMac == "": sMMac = sMac
    if sUsername == "": sUsername = username
    if sPwd == "": sPwd = pwd
    if sP == "": sP = sPort
    if sSys == "": sSys = sSystem
    otc = open_thor_operation(sDmac,sMMac,sUsername,sPwd,sP,sSys)
    #otc = openThorWindow(devMac,sMac)
    otc.open_thor_win()

def icsp_random_switch(input,output,times):
    u'''
    random switch the input and output
    @param:
    input: input num
    output: output num
    times:  run times
    @return: a boolean 
    '''
    #init the parameter for RobotFramework
    input = int(input)
    output = int(output)
    times = int(times)
    
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
        #print 'after set, the matrix:' 
        #print matrix
        logger.prt.info("after set, the matrix is:")
        logger.prt.info(matrix)
        #send command to device
        command='CI'+sInput+'O'+sOutput
        #print 'send command is:'+command
        logger.prt.info("CI"+sInput+"O"+sOutput)
        command_thor_test(command)
        newMatrix = get_matrix(input,output+2)
        #print newMatrix
        logger.prt.info(newMatrix)
        if(len(list)<output):
            if(compare_matrix(matrix, newMatrix)):
                continue
            else:
                #print 'Input:'+sInput+'Output:'+sOutput
                logger.prt.error("Input:"+sInput+"Output:"+sOutput)
                return False
        else:
            matrix[int(sInput)-1][output]=1
            #print matrix
            logger.prt.info("all port after set matrix is :")
            logger.prt.info(matrix)
            if(compare_matrix(matrix, newMatrix)):
                continue
            else:
                #print 'Input:'+sInput+'to all failed'
                logger.prt.error("Input:"+sInput+"to all failed")
                return False
    return True

def icsp_order_switch(input,output):
    u'''
    @param: 
    input: input port
    output: output port
    @return: Boolean
    Ordered switch the input to output port 
    '''
    #init the parameter for RobotFramework
    input = int(input)
    output = int(output)
     
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
    
if __name__ == '__main__':
    #print get_matrix(8, 10)
    #print order_swtich(8, 8)
    #print random_switch(8,8,10)
    open_thor_command()