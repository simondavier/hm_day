#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial
import serial.tools.list_ports

class SerialConnection(object):
    def __init__(self,sBaud=115200,timeout=1):
        self.fd=None
        try:
            self.fd = serial.Serial(self.get_serial_name(),sBaud,timeout = 1)
        except RuntimeError as e:
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
                if "Prolific USB-to-Serial Comm Port (" in str1:
                    sName = s_port[0]
                    return sName
    
    def send_cmd1(self,cmd):
        self.fd.write((cmd+'\r').encode("utf-8"))
        self.fd.readline()
        response = self.fd.readline()
        return response
    
    def send_cmd(self,cmd):
        self.fd.write((cmd+'\r').encode("utf-8"))
        return self.fd.readlines()
    
    def serial_close(self):
        try:
            self.fd.close()
            return 0
        except:
            return -1
    
"""if __name__ == '__main__':
    fd = SerialConnection()
    
    cmd = 'fmtl?'
    print (fd.send_cmd1(cmd))
        
    cmd = 'ifau'
    print (fd.send_cmd1(cmd))
    
    cmd = 'ifad? 82'
    print (fd.send_cmd1(cmd))
    
    fd.serial_close()"""