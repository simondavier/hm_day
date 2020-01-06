#!/usr/bin/env python
# -*- coding: utf-8 -*-

import switchconfig_operation
import xml.etree.ElementTree as ET
import telnet_operation1 as telnet
import sys
import os
import ctypes
import json
import time
import logging as log
from logging import handlers

# logname = time.strftime("%Y%m%d_%H%M%S")+".log"
# print(logname)
# #log.basicConfig(filename=logname, filemode="w", level=log.DEBUG, format="[%(asctime)s]%(name)s:%(levelname)s:%(message)s")
# log.basicConfig(filename="simonout.log", filemode="w", level=log.DEBUG)
# logger = log.getLogger(__name__)
# log.debug("This is debug!")
# log.info("This is info!")
# log.warning("This is warning!")
#
# logger = log.getLogger(__name__)
# logger.setLevel(level=log.INFO)
# handler = log.FileHandler('simonout.log')
# formatter = log.Formatter('%(asctime)s]%(name)s:%(levelname)s:%(message)s')
# handler.setFormatter(formatter)
# log._addHandlerRef(handler)

filelist="D:\\Videotool_TCL\\VideoTool\\QuantumDataFiles\\filelist.txt"
xmlpath = "D:\\Videotool_TCL\\VideoTool\\QuantumDataFiles\\EDIDs\\"
edidxlsx = "D:\\TestStandDemo\\VideoSwtich\\QdEDID.xlsx"
str = 'IFAD? 82\n\rAVI InfoFrame ver. 2:\r\nColor space: RGB Default Range\r\nVideo ID: 4 (1280 x 720 p @ 59.94/60Hz 16:9)\r\nActive AR same as Coded\r\nNon-uniform Scaling: None known\r\nPixels repeated 0 times.\r\nChecksum OK. Version=2, Length=13\r\nRaw data: 82 02 0D 53 10 08 00 04 00 00 00 00 00 00 00 00 00 \r\n\n\rR:\\> '
import re

import logging
from logging import handlers

class Logger(object):
    level_relations = {
        'debug':logging.DEBUG,
        'info':logging.INFO,
        'warning':logging.WARNING,
        'error':logging.ERROR,
        'crit':logging.CRITICAL
    }#日志级别关系映射

    def __init__(self,filename,level='info',when='D',backCount=3,fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)#设置日志格式
        self.logger.setLevel(self.level_relations.get(level))#设置日志级别
        sh = logging.StreamHandler()#往屏幕上输出
        sh.setFormatter(format_str) #设置屏幕上显示的格式
        th = handlers.TimedRotatingFileHandler(filename=filename,when=when,backupCount=backCount,encoding='utf-8')#往文件里写入#指定间隔时间自动生成文件的处理器
        #实例化TimedRotatingFileHandler
        #interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        th.setFormatter(format_str)#设置文件里写入的格式
        self.logger.addHandler(sh) #把对象加到logger里
        self.logger.addHandler(th)
if __name__ == '__main__':
    log = Logger('all.log',level='debug')
    log.logger.debug('debug')
    log.logger.info('info')
    log.logger.warning('警告')
    log.logger.error('报错')
    log.logger.critical('严重')
    Logger('error.log', level='error').logger.error('error')

# def addedidToExcel():
#     sco = switchconfig_operation.SwitchConfigOperation(edidxlsx)
#
#     with open(filelist, 'r') as fd:
#         lists = fd.readlines()
#     for i in range(0,len(lists)):
#         lists[i] = lists[i].strip('\n').split('.')[0]
#     #print(lists)
#     i=2
#     for code in lists:
#         xmlfile=xmlpath+code+'.xml'
#         try:
#             tree = ET.parse(xmlfile)
#             root = tree.getroot()
#         except:
#             raise ('parse %s failed!' % xmlfile)
#         block0 = root[1][0].text
#         block1 = root[1][1].text
#         sco.setCellValue(i, 1, code)
#         sco.setCellValue(i, 2, block0)
#         sco.setCellValue(i, 3, block1)
#         i+=1
#     else:
#         sco.saveModify(edidxlsx)
#
# def test():
#     #str="{"HDMI1":1,HDMI2:2,HDMI3:3,HDMI4:4,HDBT1:5,HDBT2:6,HDBT3:7,HDBT4:8}"
#     str = "HDMI1:1,HDMI2:2,HDMI3:3,HDMI4:4,HDBT1:5,HDBT2:6,HDBT3:7,HDBT4:8"
#     #print(eval(str))
#     dic={}
#     l = str.split(',')
#     for opt in l:
#         #print(opt.split(':'))
#         dic[opt.split(':')[0]]=opt.split(':')[1]
#     #print (dic)
#     l = dic.values()
#     #log.INFO(list(l))
#     print(list(l))
#     # print(dic.keys())
#     # print(dic.items())
#
def test1():
    filename="simon.log"
    logger = log.getLogger(filename)
    logger.setLevel(level=log.DEBUG)
    #handler = log.FileHandler('simonout.log')
    formatter = log.Formatter('%(asctime)s]%(name)s:%(levelname)s:%(message)s')
    #handler.setFormatter(formatter)
    #log.basicConfig(filename="simonout.log", filemode="a")
    th = handlers.TimedRotatingFileHandler(filename=filename, encoding='utf-8')
    th.setFormatter(formatter)
    logger.addHandler(th)
    log.debug("This is debug!")
    log.info("This is info!")
    log.warning("This is warning!")
#
#
# if __name__ == '__main__':
    #addedidToExcel()
    # tn = telnet.TelnetApp('192.168.2.113','administrator','password')
    # #tn.send_thor_cmd('32003:7:1', '?vidout_scale')
    # tn.send_thor_cmd('32006:1:1', 'ci3oall')
    # str1 = "".join(re.findall(r".*(\d.:\d)", str))
    # print (str1)
    test1()