#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on Jul 3, 2018
@author: WiShen
'''

#import os
#import sys
import logging
import time

sLevelDft = "Warning"   #default log level is warning
sToFileDft = "False"    #default is NOT write to file just console only
sFormat = "%(asctime)s [%(levelname)s] %(filename)s(%(lineno)d): %(message)s"
sFile = "./Logs/AutoTest_" + time.strftime("%Y%m%d_%H%M%S") + ".log"
handler = None
prt = None

def initLogger():
    '''
    initiate the logger object, it's mandatory
    '''
    global sFormat, sLevelDft, prt
    logging.basicConfig(format = sFormat)
    prt = logging.getLogger()
    prt.setLevel(sLevelDft.upper())

def cfgLevel(sLevel):
    '''
    Log level from low to high(case insensitive):  \n
    debug, info, warning, error, critical
    '''
    global sLevelDft, prt
    try:
        prt.setLevel(sLevel.upper())
        try:
            handler.setLevel(sLevel.upper())
        except: pass
        sLevelDft = sLevel
    except:
        prt.warning("Log level " + sLevel + " is wrong!")
        pass
        
def cfgToFile(sToFile):
    '''
    Configure the log if write to file \n
    True: write to file \n
    False: never write to file, console print only \n
    '''
    global sFormat, sFile, handler, prt
    if sToFile.upper() == "TRUE":
        handler = logging.FileHandler(sFile)
        handler.setFormatter(logging.Formatter(sFormat))
        prt.addHandler(handler)
    
'''
def debug(sMsg):
    prt.debug(sMsg)

def info(sMsg):
    prt.info(sMsg)

def warning(sMsg):
    prt.warning(sMsg)

def error(sMsg):
    prt.error(sMsg)

def critical(sMsg):
    return prt.critical(sMsg)
'''

#print os.path.basename(__file__)
#print os.path.basename(sys.argv[0])

