# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 14:56:00 2018

@author: WeicZhang
"""
import telnet_library_for_RF as tlfr
import logger
import icsp_operation as io

logger.cfgLevel("debug")
class telnetApp(object):
    def __init__(self):
        self.tn = None
        self.output = ''
        self.status = -1
    def build_connection(self,loginIp,loginUser,loginPwd):
        self.tn = tlfr.build_connection(loginIp,loginUser,loginPwd)
    def send_command(self,command):
        io.click_ClearList()
        tlfr.excut_command(self.tn,command)
        io.time.sleep(0.5)
        self.out = io.get_comeback_message()
    def kill_connection(self):
        self.status=tlfr.kill_connection(self.tn)
        if self.status==0:
            logger.prt.debug('telnet killed normally')
        elif self.status==-1:
            logger.prt.debug('telnet not killed, abnormal happen!')
        else:
            logger.prt.debug("telnet kill, not expected case happen!")