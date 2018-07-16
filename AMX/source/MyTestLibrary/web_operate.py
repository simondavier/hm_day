#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on Jun 28, 2018
@author: WiShen
'''

import sys
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import logger

logger.initLogger()

class webApp(object):
    def __init__(self):
        option = webdriver.ChromeOptions()
        option.add_argument('disable-infobars')
        self.driver = webdriver.Chrome(chrome_options = option )
        self.driver.maximize_window()  #maximize chrome
        self.result = False

################ login and open web functions #################
    def login(self, sLoginIp, sLoginPwd):
        loginUrl = "http://" + sLoginIp
        self.driver.get(loginUrl)
        self.driver.implicitly_wait(10)
        #print self.driver.title
        if self.driver.title == sLoginIp:
            #print "can not open web GUI!"
            logger.prt.critical("can not open web GUI in " + sLoginIp)
            self.result = False
            self.close()
            sys.exit()
        else:
            self.result = True
        
        inputPwd = self.driver.find_element_by_id('password')   #find password input box, ***special element***
        inputPwd.send_keys(sLoginPwd)
        btnLogin = self.driver.find_element_by_id('loginBtn')   #find login input box, ***special element***
        btnLogin.click()
        time.sleep(10)

    def close(self):
        self.driver.quit()
        logger.prt.info("close the chrome.")
    
    def click_matrix(self):
        self.click_element("Matrix Control", "link")  #***special element***
        time.sleep(2)
    
    def click_admin(self, sAdminPwd):
        self.click_element("Admin Setting", "link")   #***special element***
        
        try:
            inputPwd = self.driver.find_element_by_id('admin-password')  #***special element***
            inputPwd.send_keys(sAdminPwd)
            time.sleep(1)
            self.click_element("//*[@id='adminLogin_dialog']/div/button", "xpath")  #***special element***
            time.sleep(1)
            inputPwd.send_keys(Keys.ESCAPE)
            logger.prt.info("input admin password and login!")
        except:
            pass
            #print "admin password not need!"
            logger.prt.info("admin password not need!")
        time.sleep(1)

################ web operation functions #################
    def select_radio(self, sRadioId):
        '''
        radioBtn = self.driver.find_element_by_id(radioId)
        #print radioBtn.tag_name
        #radioBtn.click()
        actChn = ActionChains(self.driver)
        actChn.move_to_element(radioBtn)
        actChn.perform()
        actChn.click(radioBtn)
        actChn.perform()
        time.sleep(3)
        '''
        self.click_element(sRadioId, "id")
        #print "select " + radioId
        logger.prt.info("select " + sRadioId)
  
    def select_matrix(self,lRadio):
        for item in lRadio:
            self.select_radio(item)

    def click_element(self,sElement,sBy):
        if sBy == "id" or sBy == "":
            webEle = self.driver.find_element_by_id(sElement)
        if sBy == "xpath":
            webEle = self.driver.find_element_by_xpath(sElement)
        if sBy == "link":
            webEle = self.driver.find_element_by_link_text(sElement)
            
        #webEle.click()
        actChn = ActionChains(self.driver)
        actChn.move_to_element(webEle)
        actChn.perform()
        time.sleep(1)
        actChn.click(webEle)
        actChn.perform()
        logger.prt.info(sElement + " is clicked.")
        time.sleep(1)

    def input_text(self, sInputBox, sInputTxt, sBy="id"):
        if sBy == "id" or sBy == "":
            inpBox = self.driver.find_element_by_id(sInputBox)
        if sBy == "xpath":
            inpBox = self.driver.find_element_by_xpath(sInputBox)

        inpBox.clear()
        inpBox.send_keys(sInputTxt)
        logger.prt.info("input content is " + inpBox.get_attribute('value'))
    
    def save_and_load(self, sBtnSave, sBtnLoad):
        self.click_element(sBtnSave, "xpath")
        time.sleep(2)
        #select matrix-video-in0-all for reseting
        self.select_radio("matrix-video-in0-all")  #***special element***
        time.sleep(3)
        self.click_element(sBtnLoad, "xpath")
        time.sleep(3)

    def select_output(self, iValue):
        # iValue is the value in output list
        lOutput = Select(self.driver.find_element_by_id("cec-port-select"))  #***special element***
        lOutput.select_by_value(str(iValue))
        logger.prt.info("output list value=" + str(iValue) + " is selected")
        time.sleep(2)
        
    def set_CEC_ctrl(self, iOutput, sOnOffXpath):
        # iValue is the value in output list
        #self.click_element("cec-port-select", "id")
        self.select_output(iOutput)
        self.click_element(sOnOffXpath, "xpath")
        logger.prt.info("CEC is set ON/OFF")
        time.sleep(2)
        
    def set_radio_onoff(self, sBtnXpath, sOnOff="on"):
        radioBtn = self.driver.find_element_by_xpath(sBtnXpath)
        bgImg = radioBtn.value_of_css_property("background-image")
        
        if sOnOff.upper() == "ON":
            if bgImg[bgImg.rindex("/")+1:-2] <> "radio-select.png":  #***special element***
                self.click_element(sBtnXpath, 'xpath')
        if sOnOff.upper() == "OFF":
            if bgImg[bgImg.rindex("/")+1:-2] <> "radio.png":  #***special element***
                self.click_element(sBtnXpath, 'xpath')
                
    def set_auto_delay(self, sBtnXpath, sInpId, iDelay):
        # iDelay is int, range is 1 - 30
        if iDelay < 1 or iDelay > 30:
            logger.prt.error("Auto control time is out of range!")
            
        self.set_radio_onoff(sBtnXpath)
        self.input_text(sInpId, str(iDelay))
        self.click_element('tabs-2','id')  #after input delay, need to click other area


        

################ verify and check functions #################
    def verify_radio_byImg(self, sRadio, sExpImg, sBy="id"):
        if sBy == "id" or sBy == "":
            radioBtn = self.driver.find_element_by_id(sRadio)
        if sBy == "xpath":
            radioBtn = self.driver.find_element_by_xpath(sRadio)

        bgImg = radioBtn.value_of_css_property("background-image")
        logger.prt.info("background image is " + bgImg[bgImg.rindex("/")+1:-2])
        if bgImg[bgImg.rindex("/")+1:-2] == sExpImg:
            self.result = True
        else:
            self.result = False
            #print radioId + " is not selectd!"
            logger.prt.error(sRadio + " is not selectd!")
    
    def verify_matrix_byImg(self, lRadio, sExpImg):
        for item in lRadio:
            self.verify_radio_byImg(item, sExpImg)
            if self.result:
                #print "test passed!"
                logger.prt.info("test is passed!")
            else:
                #print "test failed!"
                logger.prt.error("test is failed!")
                break

    def verify_input_text(self, sInput, sExpTxt, sBy="id"):
        if sBy == "id" or sBy == "":
            inputBox = self.driver.find_element_by_id(sInput)
        if sBy == "xpath":
            inputBox = self.driver.find_element_by_xpath(sInput)
        
        if inputBox.get_attribute('value') == sExpTxt:
            self.result = True
        else:
            self.result = False
            logger.prt.error(sInput + " is not euqal to " + sExpTxt)

    def verify_auto_ctrl(self, sRadXpath, sInputId, iOutput, iDelay, sOnOff="on"):
        if iOutput <> 1:
            iChkOutput = 1
        else:
            iChkOutput = 2
        self.select_output(iChkOutput)  #change select to other output
        self.select_output(iOutput)     #select back to target output
        
        if sOnOff.upper() == "ON":
            self.verify_radio_byImg(sRadXpath, "radio-select.png", "xpath")  #***special element***
            self.verify_input_text(sInputId, str(iDelay), "id")
        if sOnOff.upper() == "OFF":
            self.verify_radio_byImg(sRadXpath, "radio.png", "xpath")  #***special element***
        
        if self.result:
            #print "test passed!"
            logger.prt.info("test is passed!")
        else:
            #print "test failed!"
            logger.prt.error("test is failed!")


