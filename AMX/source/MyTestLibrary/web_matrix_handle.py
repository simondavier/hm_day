#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on Jun 29, 2018
@author: WiShen
'''

import ConfigParser

def get_matrix(fConf, iPreset):
    '''
    Get the read the special section from 9*9 matrix in configuration file, \n
    and output a list of radio id which format is same as webpage. \n
    fConf: configuration file name; \n
    iPreset: the number of sectoin in conf file.
    '''
    cf = ConfigParser.ConfigParser()
    cf.read(fConf)
    sect = cf.sections()[iPreset-1]
    lRadio = []
    
    for item in cf.items(sect):
        print "item="+str(item)
        if return_radio(item) <> []:
            print return_radio(item)
            lRadio =  lRadio + return_radio(item)
    
    return lRadio

def return_radio(lItem):
    '''
    input a line format like as "'in1', '0,0,0,0,0,0,0,1,0'", \n
    output a radio string format like as "matrix-video-in1-out8" \n
    lItem: list which read from conf file.
    '''
    lReturn = []
    sRadio = "matrix-video-" + lItem[0] + "-"
    lValue = list(eval(lItem[1]))
    #print lValue
    
    j = 0
    for i in lValue:
        j = j + 1
        if i <> 0 and j < 9:
            sTemp = sRadio + "out" + str(j)
            lReturn.append(sTemp)
            
        if i <> 0 and j == 9:
            sTemp = sRadio + "all"
            lReturn.append(sTemp)
    
    return lReturn

'''
if __name__ == '__main__':
    get_matrix("web_matrix_0808.conf", 2)
'''
