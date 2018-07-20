# -*- coding: utf-8 -*-

import autoit as ai
from icsp_module import *
import time
import re
import random

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
    
if __name__ == '__main__':
    #print get_matrix(8, 10)
    #print order_swtich(8, 8)
    print random_switch(8,8,10)