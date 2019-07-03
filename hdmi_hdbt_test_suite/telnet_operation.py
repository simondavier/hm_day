#!/usr/bin/env python
# -*- coding:utf-8 -*-

import telnetlib
import time
import re
class TelnetApp(object):
    def __init__(self,sIpAddress,sLoginName,sLoginPassword):
        u'''
        @parameter:\n
        sIpAddress is ip address of telnet to connected \n
        sLoginName is device's login name  \n
        sLoginPassword is device's password     \n
        @return:            \n
        an telnet object,which is used in other method "excut_command" and  "kill_connection"
        '''
        self.tn = None
        self.out_str = ''
        try:
            self.tn = telnetlib.Telnet(sIpAddress,23,5)
            try:
                self.tn.read_until(b"\r\nLogin : ",2)
            except:
                self.tn.read_until(b"\r\n>",1)
            time.sleep(2)
            self.tn.write((sLoginName+'\r\n').encode('utf-8'))
            time.sleep(1)
            self.tn.write((sLoginPassword+'\r\n').encode('utf-8'))
            time.sleep(0.5)
            self.out_str = self.tn.read_very_eager().decode('ascii')
            #print(self.out_str)
            if  'Invalid username and/or password or user account is temporarily locked out'  in self.out_str:
                #print('this username '+sLoginName+' or password '+sLoginPassword+ ' is invalid!!!')
                raise ValueError
        except ValueError:
            raise ValueError('this USERNAME '+sLoginName+' or PASSWORD: '+sLoginPassword+ ' is invalid!!!')
        except Exception:
            raise RuntimeError('this IP '+sIpAddress+' could not connected by telnet!!!')
        
    def excut_command(self,command):
        self.tn.write((command+'\r\n').encode('utf-8'))
        #self.tn.write((command)+'\r')
        time.sleep(1)
        out=self.tn.read_very_eager().decode('ascii')
        return out

    def send_thor_cmd(self,dps,cmd):
        self.excut_command('send command '+dps+',\"\''+cmd+'\'\"')
    
    def kill_connection(self):
        try:
            self.tn.close()
            return 0
        except:
            return -1
        
    def parse_get_device_and_ip(self,sInputs):
        u'''
        this function is used for parse the telnet commmand "show device" \n
        @reutrn:        \n
        output is 3 list: device number, device name, ip address \n
        @param :        \n
         return value of telnet command "show device"       \n
        For example:        \n
        dNumber,dName,dIP = parse_get_device_and_ip(sInput)
        '''
        
        xx = sInputs.split('\r\n')
        yy=[]
        for i in xx:
            for j in i.split(u'  '):#split the \r\n and  '  '
                yy.append(j.encode('unicode-escape').decode('string-escape'))
        count = 0
        for i in range(0,len(yy)):
            if yy[i]=='':
                count+=1        #remove count times u''
        for i in range(0,count):
            yy.remove('')
        #return yy
        pattern  = re.compile(r'^[0-9]{5}$')
        pattern2 = (r'Physical Address')
        device_number = []
        device_name = []
        device_serial = []
        ip = []
        for i in range(0,len(yy)): #find the five number and physical address
            if pattern.match(yy[i]) != None:
                device_number.append(yy[i])
                device_name.append(yy[i+1])
            if yy[i].find('Pings') >=0:# the item befor "Failed Pings=0"
                device_serial.append(yy[i-1])
            if (yy[i].find(pattern2))==1:
                ip.append(yy[i].replace(' Physical Address=IP ',''))
            
        return device_number,device_name,ip,device_serial
    
    def parse_get_ip(self,sInput):
        u'''
        sIput is the return message of telnet command "get ip" \n
        @return is the dictionary, the example is:    \n
        {'DHCP:': 'true',               \n
         'Gateway:': '192.168.1.1',       \n      
         'Hostname:': 'AMX-PR01-0808-8064DC',\n
         'IP Address:': '192.168.1.100',\n
         'Netmask:': '255.255.255.0'}
        '''
        xx = sInput.splitlines(False)
        yy=[]
        out={}
        for i in xx:
            for j in i.split(u'  '):#split the \r\n and  '  '
                yy.append(j.encode('unicode-escape').decode('string-escape'))
        count = 0
        for i in range(0,len(yy)):
            if yy[i]=='':
                count+=1        #remove count times u''
        for i in range(0,count):
            yy.remove('')
        
        for i in range(0,len(yy)):
            yy[i]=yy[i].strip()
            if yy[i].find('Hostname')>=0 or yy[i].find('IP Address')>=0 or \
            yy[i].find('Netmask')>=0 or yy[i].find('Gateway')>=0 or \
            yy[i].find('DHCP')>=0:
                out[yy[i]]=yy[i+1].strip()
        return out
      
    def parse_get_connection(self,sInput):
        u'''
        sIput is the return message of telnet command "get connection" \n
        @return is the dictionary, the example is:    \n
        {'Connection Mode:': 'ndp',                 \n
         'Master Ip/URL': '192.168.1.103',          \n
         'Master Port:': '1319',                    \n
         'System Number:': '1'}
        '''
        xx = sInput.splitlines(False)
        yy=[]
        out={}
        for i in xx:
            for j in i.split(u'  '):#split the \r\n and  '  '
                yy.append(j.encode('unicode-escape').decode('string-escape'))
        count = 0
        for i in range(0,len(yy)):
            if yy[i]=='':
                count+=1        #remove count times u''
        for i in range(0,count):
            yy.remove('')
        #return yy
        for i in range(0,len(yy)):
            yy[i]=yy[i].strip()
            if yy[i].find('Connection Mode')>=0 or yy[i].find('System Number')>=0 or \
               yy[i].find('Master Ip/URL')>=0 or yy[i].find('Master Port')>=0:
                out[yy[i]]=yy[i+1].strip()
        return out
    
    def parse_set_friendlyname(self,sInput):
        u'''
        the input is return message of telnemt command "set friendlyname"\n
        set friendlyname\r 's return message is  like this:
           please input friendlyname:
           old friendlyname:heh  new friendlyname:
           Cancel this setting
        parse to get the current friendlyname (eg,heh)
        
        '''
        xx = sInput.splitlines(False)
        out=''
        try:
            out=xx[2].split('friendlyname:')[1].split('new')[0].strip()
        except:
            out=xx[3].split('friendlyname:')[1].split('new')[0].strip()
        return out

     

    def parse_set_location(self,sInput):
        u'''
        the input is return message of telnemt command "set location"\n
        set connection\r 's return message is  like this:
           please input location:
           old location:haha  new location:
           Cancel this setting 
        parse to get the current friendlyname
        '''
        xx = sInput.splitlines(False)
        print (xx)
        out=''
        try:
            out=xx[2].split('location:')[1].split('new')[0].strip()
        except:
            out=xx[3].split('location:')[1].split('new')[0].strip()
        return out   

    def parse_dns_list(self,sInput):
        u'''
        check dns list 1# and dns 2#
        the command is "dns list"
        DNS List:
        DNS #1:    192.168.1.1
        DNS #2:    8.8.8.8
        '''
        xx = sInput.splitlines(False)
        print (xx)
        out=[]
        for i in xx:
            temp = i.split('DNS #1:')
            temp1= i.split('DNS #2:')
            if len(temp)>=2:
                out.append(temp[1].strip())
            elif len(temp1)>=2:
                out.append(temp1[1].strip())
        print (out)
        return out
        
         
         
         
         
         
         
         
         
