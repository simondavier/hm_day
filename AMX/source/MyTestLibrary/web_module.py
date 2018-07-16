#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on Jun 28, 2018
@author: WiShen
'''

#import time
import web_operate
from web_matrix_handle import get_matrix
import logger

ROBOT_LIBRARY_SCOPE = "GLOBAL"
ROBOT_EXIT_ON_FAILURE = True

sIpDft = "192.168.1.4"
sPwdDft = "admin"
sAdmPwdDft = "123456"
fMatrixDft = "web_matrix_0808.conf"
myWeb = None

def set_log(sLogLevel="info",isToFile="False"):
    '''
    Set log level and if wite to file \n
    This method maybe not use.
    '''
    logger.initLogger()
    logger.cfgToFile(isToFile)    
    logger.cfgLevel(sLogLevel)

def setup_web(sIp="", sPwd="", sAdmPwd="", fMatrix=""):
    '''
    Setup web application object for later test operation. \n
    sIp: 0808 device IP, default is 192.168.1.4 \n
    sPwd: 0808 login password, default is admin \n
    sAdmPwd: 0808 admin password, default is 123456 \n
    fMatrix: 0808 9*9 matrix configureation file, default is web_matrix_0808.conf
    '''
    global sIpDft, sPwdDft, sAdmPwdDft, fMatrixDft, myWeb
    if sIp <> "": sIpDft = sIp
    if sPwd <> "": sPwdDft = sPwd
    if sAdmPwd <> "": sAdmPwdDft = sAdmPwd
    if fMatrix <> "": fMatrixDft = fMatrix
    
    myWeb = web_operate.webApp()

def login_web():
    '''
    Login web GUI action, not need parameter.
    '''
    myWeb.login(sIpDft, sPwdDft)
    
def close_web():
    '''
    Close web GUI action, not need parameter.
    '''
    myWeb.close()
    
def click_matrix():
    '''
    Click "Matrix Control" tab and open the webpage in 0808 web GUI.
    '''
    myWeb.click_matrix()
    
def click_admin():
    '''
    Click "Admin Setting" tab and open the webpage in 0808 web GUI. \n
    the first visit will input admin password with the parameter sAdmPwd.
    '''
    myWeb.click_admin(sAdmPwdDft)

def set_switch_one(iSect):
    '''
    Set switch with one configured matrix and verify.\n    
    iSect: the section number in matrix_0808.conf.\n
    '''
    lRadio = get_matrix(fMatrixDft,iSect)
    myWeb.select_matrix(lRadio)
    myWeb.verify_matrix_byImg(lRadio, "radio-select.png")

def set_switch_multi(iSect):
    '''
    Set switch from 1 to [iSect] configured matrix and verify \n
    iSect: the section number in matrix_0808.conf \n
    matrix_0808.conf should configure not less than iSect sections \n
    '''
    i = 1
    while (i <= iSect):
        lRadio = get_matrix(fMatrixDft,i)
        myWeb.select_matrix(lRadio)
        myWeb.verify_matrix_byImg(lRadio, "radio-select.png")
        i = i + 1

def test_presets_one(iSect):
    '''
    Set preset with one configured matrix and verify \n
    iSect: the section number in web_matrix_0808.conf \n
    '''
    sBtnSave = "//*[@id='matrix-contain']/div[2]/div/fieldset[" + str(iSect) + "]/button[1]"
    sBtnLoad = "//*[@id='matrix-contain']/div[2]/div/fieldset[" + str(iSect) + "]/button[2]"
    lRadio = get_matrix(fMatrixDft,iSect)
    myWeb.select_matrix(lRadio)
    myWeb.save_and_load(sBtnSave, sBtnLoad)
    myWeb.verify_matrix_byImg(lRadio, "radio-select.png")

def test_presets_multi(iSect):
    '''
    Set preset from 1 to [iSect] section in configured matrix and verify \n
    iSect: the section number in matrix_0808.conf \n
    web_matrix_0808.conf should configure not less than iSect sections \n
    '''
    i = 1
    while (i <= iSect):
        sBtnSave = "//*[@id='matrix-contain']/div[2]/div/fieldset[" + str(i) + "]/button[1]"
        sBtnLoad = "//*[@id='matrix-contain']/div[2]/div/fieldset[" + str(i) + "]/button[2]"
        lRadio = get_matrix(fMatrixDft,i)
        myWeb.select_matrix(lRadio)
        myWeb.save_and_load(sBtnSave, sBtnLoad)
        myWeb.verify_matrix_byImg(lRadio, "radio-select.png")
        i = i + 1

def set_CEC_one(iOutput, sOnOff):
    '''
    Set one output CEC "on" or "off" \n
    iOutput: select output list value, 1 - 12 \n
    sOnOff: set CEC "on" or "off" (case insensitive) \n
    '''
    sBtnDisOn = "//*[@id='tabs-2']/div/div/div/fieldset/div/table/tbody/tr/td[2]/button[1]"
    sBtnDisOff = "//*[@id='tabs-2']/div/div/div/fieldset/div/table/tbody/tr/td[2]/button[2]"
    if sOnOff.upper() == "ON":
        myWeb.set_CEC_ctrl(iOutput, sBtnDisOn)
    if sOnOff.upper() == "OFF":
        myWeb.set_CEC_ctrl(iOutput, sBtnDisOff)

def set_CEC_all(sOnOff):
    '''
    Set all output(total 13) CEC "on" or "off" \n
    sOnOff: string, "on" or "off" (case insentive) \n
    '''
    if sOnOff.upper() == "ON":
        sBtnDis = "//*[@id='tabs-2']/div/div/div/fieldset/div/table/tbody/tr/td[2]/button[1]"
    else:
        sBtnDis = "//*[@id='tabs-2']/div/div/div/fieldset/div/table/tbody/tr/td[2]/button[2]"
    
    i = 1
    while (i < 13):
        myWeb.set_CEC_ctrl(i, sBtnDis)
        i = i + 1
    
def set_auto_ctrl(iOutput, iDelay, sOnOff="on"):
    '''
    Set one output auto control ON and delay [iDelay] minutes \n
    iOutput: int, range [1,13] \n
    iDelay: int, range [1,30] \n
    sOnOff: set auto contorl "on" or "off" \n
    '''
    sRadOnOff = "//*[@id='tabs-2']/div[1]/div[1]/div/fieldset/div/table/tbody/tr[2]/td[2]/div/div[1]/label/i"
    sInpDelay = "cec-delay-time-spinner"
    myWeb.select_output(iOutput)
        
    if sOnOff.upper() == "ON":
        myWeb.set_auto_delay(sRadOnOff, sInpDelay, iDelay)
        myWeb.verify_auto_ctrl(sRadOnOff, sInpDelay, iOutput, iDelay, "on")
        
    if sOnOff.upper() == "OFF":
        myWeb.set_radio_onoff(sRadOnOff, "off")
        myWeb.verify_auto_ctrl(sRadOnOff, sInpDelay, iOutput, iDelay, "off")

'''
if __name__ == '__main__':
    #setup_web(sIpDft="192.168.1.2")
    #print sIp
'''
    #myWeb = web_operate.webApp()
    #myWeb.login(sIp, sPwd)
    
    #myWeb.click_admin(sAdmPwd)
    #myWeb.click_matrix()
    
    #set_switch_one(7)
    #set_switch_multi(3)
    #test_presets_one(1)
    #test_presets_multi(3)
    #set_CEC_one(3,"on")
    #set_CEC_all("off")
    #set_auto_ctrl(1,2,"on")
    
    #time.sleep(5)
    #myWeb.close()

    
    