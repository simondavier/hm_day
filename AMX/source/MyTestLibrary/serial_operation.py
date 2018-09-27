#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial
import serial.tools.list_ports

def get_serial_name():
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

def open_serial_port(sName):
    try:
        serialFd = serial.Serial(sName,115200,timeout = 1)
    except Exception, e:
        raise RuntimeError("Can not connect the serial!")
    return serialFd

def send_cmd1(serialFd,cmd):
    serialFd.write(cmd+'\r')
    serialFd.readline()
    response = serialFd.readline()
    return response

def send_cmd(serialFd,cmd):
    serialFd.write(cmd+'\r')
    return serialFd.readlines()

if __name__ == '__main__':
    sName = get_serial_name()
    fd = open_serial_port(sName)
    cmd = 'fmtl?'
    print send_cmd(fd, cmd)
        
    cmd = 'ifau'
    print send_cmd(fd, cmd)
    
    cmd = 'ifad? 82'
    print send_cmd(fd, cmd)