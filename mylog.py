# -*- coding: utf-8 -*-

#  mylog.py
#
#  ~~~~~~~~~~~~
#
#  Function log
#
#  ~~~~~~~~~~~~
#
#  ------------------------------------------------------------------
#  Author : Li Yonghu
#  Build: 11.06.2021
#  Last change: 11.06.2021 Li Yonghu 
#
#  Language: Python 3.7
#  ------------------------------------------------------------------
#  GNU GPL
#  
 
#

# Module Imports

import logging
import os
 
class Logger:
  def __init__(self, path,clevel = logging.DEBUG,Flevel = logging.DEBUG):
   self.logger = logging.getLogger(path)
   self.logger.setLevel(logging.DEBUG)
   fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
   #设置CMD日志
   sh = logging.StreamHandler()
   sh.setFormatter(fmt)
   sh.setLevel(clevel)
   #设置文件日志
   fh = logging.FileHandler(path)
   fh.setFormatter(fmt)
   fh.setLevel(Flevel)
   self.logger.addHandler(sh)
   self.logger.addHandler(fh)
 
  def debug(self,message):
   self.logger.debug(message)
 
  def info(self,message):
   self.logger.info(message)
 
  def war(self,message):
   self.logger.warn(message)
 
  def error(self,message):
   self.logger.error(message)
 
  def cri(self,message):
   self.logger.critical(message)

if __name__ == "__main__":
    mylogger = Logger('123.log')
    mylogger.error('111111')
    mylogger.info('222222')
    mylogger.cri('233333')
    mylogger.debug('444444')
