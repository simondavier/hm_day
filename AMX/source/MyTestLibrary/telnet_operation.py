# -*- coding: utf-8 -*-
"""
Created on Mon May  7 11:38:18 2018

@author: WeicZhang
"""



import telnetlib
import time
import re
class TelnetApp(object):
    def __init__(self,sIpAddress,sLoginName,sLoginPassword):
        self.tn = None
   # def build_connection(self,sIpAddress,sLoginName,sLoginPassword):
        u'''
        @parameter:\n
        sIpAddress is ip address of telnet to connected \n
        sLoginName is device's login name  \n
        sLoginPassword is device's password     \n
        @return:            \n
        an telnet object,which is used in other method "excut_command" and  "kill_connection"
        '''
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
            out_str = self.tn.read_very_eager().decode('ascii')
            print(out_str)
            #return out_str
            if  'Invalid username and/or password or user account is temporarily locked out'  in out_str:
                print('this username '+sLoginName+'or password'+sLoginPassword+ 'is invalid!!!')
                raise ValueError('this USERNAME: '+sLoginName+' or PASSWORD: '+sLoginPassword+ ' is invalid!!!')
                #throwerror(sLoginName,sLoginPassword)
                #return
        except ValueError:
            raise SystemError('this USERNAME '+sLoginName+' or PASSWORD: '+sLoginPassword+ ' is invalid!!!')
        except Exception:
            raise SystemError('this IP '+sIpAddress+' could not connected by telnet!!!')
    def excut_command(self,command):
        self.tn.write((command+'\r\n').encode('utf-8'))
        time.sleep(1)
        out=self.tn.read_very_eager().decode('ascii')
        return out
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
        ip = []
        for i in range(0,len(yy)): #find the five number and physical address
            if pattern.match(yy[i]) != None:
                device_number.append(yy[i])
                device_name.append(yy[i+1])
            if (yy[i].find(pattern2))==1:
                ip.append(yy[i].replace(' Physical Address=IP ',''))
            
        return device_number,device_name,ip   
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
        