#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial
import serial.tools.list_ports
import time
import re

class SerialConnection(object):
    def __init__(self,sBaud=115200,timeout=1):
        self.fd=None
        try:
            self.fd = serial.Serial(self.get_serial_name(),sBaud,timeout = 1)
        except Exception as e:
            raise RuntimeError("Can not connect the serial!")
        
    def get_serial_name(self):
        #get all com ports
        plist = list(serial.tools.list_ports.comports())
        
        if len(plist) <= 0:
            raise RuntimeError("The Serial port can't find!")
        else:
            for i in range(len(plist)):
                s_port=list(plist[i])
                str1 =''.join(list(plist[i]))
                #if "Prolific USB-to-Serial Comm Port (" in str1:
                if "COM6" in str1:
                    sName = s_port[0]
                    print(sName)
                    return sName
    
    def send_cmd1(self,cmd):
        self.fd.write((cmd+'\r').encode("utf-8"))
        print("SendCMD:" + cmd)
        time.sleep(2)
        response = self.fd.read_all().__str__()
        return response

    """def send_cmd(self,cmd):
        self.fd.write(cmd+'\r')
        return self.fd.readlines()
    """
    def send_cmd2(self,cmd):
        #self.fd.write(cmd+'\r')
        self.fd.write(bytes(cmd+'\r', encoding="utf8"))
        return self.fd.readlines()
        #return str(self.fd.readlines(), encoding="utf8")
    def send_cmd(self,cmd):
        self.fd.write((cmd+'\r').encode("utf-8"))
        #print("SendCMD:" + cmd)
        time.sleep(2)
        response = self.fd.read_all().__str__()
        response = "".join(re.findall(r"([\d]\.?)",response))
        return response

    def send_cmd_ar(self,cmd):
        self.fd.write((cmd+'\r').encode("utf-8"))
        time.sleep(2)
        response = self.fd.read_all().__str__()
        return response

    def send_cmd_ar1(self,cmd):
        self.fd.write((cmd+'\r').encode("utf-8"))
        time.sleep(2)
        response = self.fd.read_all().__str__()
        print(response)
        return response
    
    def serial_close(self):
        try:
            self.fd.close()
            return 0
        except:
            return -1
    
if __name__ == '__main__':
    fd = SerialConnection()
    
    cmd = 'fmtl?'
    print (fd.send_cmd(cmd))
        
    cmd = 'ifau'
    print (fd.send_cmd(cmd))
    
    cmd = 'ifad? 82'
    print (fd.send_cmd(cmd))
    
    fd.serial_close()