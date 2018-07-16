# -*- coding: utf-8 -*-
"""
Created on Mon May  7 11:38:18 2018

@author: WeicZhang
"""
# =============================================================================
# import telnetlib
# import time
# 
# 
# def telnetip(tnip,username,password,cmd):
#     # 连接Telnet服务器
#     tn = telnetlib.Telnet(tnip, port=23, timeout=50)
#     # 输入登录用户名
#     tn.read_until(b"\r\nLogin : ")
#     tn.write(username+b'\r\n')
#     time.sleep(1)
#     #tn.read_very_eager()
#     #tn.read_until(b"\r\nPassword : ")
#     tn.write(password+b'\r\n')
#     #tn.write(b'help\r\n')
#     tn.write(cmd)
#     time.sleep(1)
#     #out=tn.read_very_eager().decode('ascii')
#     out=tn.read_lazy().decode('ascii')
#     tn.close()
#     return out
# 
#    
# 
# if __name__ == '__main__':
#     # 配置选项
#     ip = '192.168.1.46'  # Telnet交换机IP
#     username = b'administrator'  # 登录用户名
#     password = b'password'  # 登录密码
#     cmd = b'pwd\r\n'
#     out=telnetip(ip,username,password,cmd)
#     print(out)
# =============================================================================




import telnetlib
import time

#password = getpass.getpass()
#def throwerror(loginname,loginpassword):
#    raise Exception('this username '+loginname+'or password'+loginpassword+ 'is invalid!!!')
#    return
def build_connection(ipaddress,loginname,loginpassword):
    try:
        tn = telnetlib.Telnet(ipaddress,23,5)
        try:
            tn.read_until(b"\r\nLogin : ",2)
        except:
            tn.read_until(b"\r\n>",1)
        time.sleep(2)
        tn.write((loginname+'\r\n').encode('utf-8'))
        time.sleep(1)
        tn.write((loginpassword+'\r\n').encode('utf-8'))
        time.sleep(0.5)
        out_str = tn.read_very_eager().decode('ascii')
        print(out_str)
        #return out_str
        if  'Invalid username and/or password or user account is temporarily locked out'  in out_str:
            print('this username '+loginname+'or password'+loginpassword+ 'is invalid!!!')
            raise ValueError('this USERNAME: '+loginname+' or PASSWORD: '+loginpassword+ ' is invalid!!!')
            #throwerror(loginname,loginpassword)
            #return
    except ValueError:
        raise SystemError('this USERNAME '+loginname+' or PASSWORD: '+loginpassword+ ' is invalid!!!')
    except Exception:
        raise SystemError('this IP '+ipaddress+' could not connected by telnet!!!')
    return tn
def excut_command(tn,command):
    tn.write((command+'\r\n').encode('utf-8'))
    time.sleep(1)
    out=tn.read_very_eager().decode('ascii')
    return out
def kill_connection(tn):
    try:
        tn.close()
        return 0
    except:
        return -1
#print(mo)
#print(tn.read_all().decode('ascii'))
#tn.close()
'''
cmdlist=['date','time','disk free','get device holdoff',
         'disk free','pwd','report firmware',
         'report netlinx','show https redirect'
         'get duet memory','get firmware',
         'mem','show mem','get icslan',
         'get leases','show combine','show log start',
         'start log on','show start log start',
         'get audit status','list audit files',
         'list audit servers','show buffers',
         'show max buffers','dns list',
         'get ip','ip status','program info',
         'show mem','boot status','get platform info',
         'show watchdog','show remote','show notify',
         'physical status','dispswitch','show system',
         'cpu usage','show route','mail status',
         'show tcp','get device traffic'      
         ]
cmdlist_new = cmdlist[:]
outputfile = open('output.csv','w',newline='')
outputwriter = csv.writer(outputfile)
outputwriter.writerow(['cmd name','return words'])
for i in range(len(cmdlist)):
    cmdlist_new[i]=cmdlist[i]+'\r\n'
    print(cmdlist_new[i])
    tn.write(cmdlist_new[i].encode('utf-8'))
    if cmdlist[i]=='cpu usage':
        time.sleep(11)
    else:
        time.sleep(2)
    out=tn.read_very_eager().decode('ascii')
    outputwriter.writerow([cmdlist[i],out])
    print(out)
    del out
tn.close()    
outputfile.close()
'''