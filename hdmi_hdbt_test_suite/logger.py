#!/usr/bin/env python
# -*- coding:utf-8 -*-
import logging
import os
from logging import handlers

class Logger(object):
    level_relations = {
        'debug':logging.DEBUG,
        'info':logging.INFO,
        'warning':logging.WARNING,
        'error':logging.ERROR,
        'crit':logging.CRITICAL
    }#level map
    def __init__(self,filename,level='info',when='D',backCount=0,fmt='[%(asctime)s]:%(levelname)s:%(message)s'):
        self.create_log()
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)#format the log
        self.logger.setLevel(self.level_relations.get(level))#set log level
        #sh = logging.StreamHandler()#screen display
        #sh.setFormatter(format_str) #set screen display format
        # Set TimedRotatingFileHandler
        th = handlers.TimedRotatingFileHandler(filename=filename,when=when,backupCount=backCount,encoding='utf-8')
        th.setFormatter(format_str)#format the writing log
        #self.logger.addHandler(sh) #add to logger
        self.logger.addHandler(th)

    def create_log(self):
        path = ".\log"
        if not os.path.exists(path):
            os.makedirs(path)
if __name__ == '__main__':
    log = Logger('all.log',level='debug')
    log.logger.debug('debug')
    log.logger.info('info')
    log.logger.warning('warning')
    log.logger.error('error')
    log.logger.critical('critical')
    Logger('error.log', level='error').logger.error('error')

