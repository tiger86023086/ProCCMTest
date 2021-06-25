# -*- coding: utf-8 -*-

#  testthread.py
#
#  ~~~~~~~~~~~~
#
#  Function GUI Test Thread
#
#  ~~~~~~~~~~~~
#
#  ------------------------------------------------------------------
#  Author : Li Yonghu
#  Build: 23.06.2021
#  Last change: 24.06.2021 Li Yonghu 
#
#  Language: Python 3.7  PyQt5.15.2
#  ------------------------------------------------------------------
#  GNU GPL
#  
 
#

# Module Imports

from PyQt5.QtCore import (Qt,QThread,QMutex,QObject)
from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtCore import pyqtSlot as Slot
import time,os
import traceback
from testsqe import TestSqe

class TestThread(QThread):
      result = Signal(bool)     
      def __init__(self,parent=None):
            super(TestThread,self).__init__(parent)           

            self.error = False
            self.completed = False           
      def initialize(self,
                     canbox,
                     canchannel,
                     dbfile,
                     flgacrun,
                     dictACFlg,
                     dictSigVal,
                     listmsgbox):            

            self.canbox = canbox
            self.canchannel = canchannel
            self.dbfile = dbfile
            self.flgacrun = flgacrun
            #self.flgsigrun = flgsigrun
            self.dictACFlg = dictACFlg
            self.dictSigVal = dictSigVal
            self.listmesgbox = listmsgbox
            
      def run(self):                 
            reflag=self.testexc(self.canbox,
                                 self.canchannel,
                                 self.dbfile,                                 
                                 self.dictACFlg,
                                 self.dictSigVal,
                                 self.listmesgbox,
                                 self.error)               
            if reflag == True:                                    
                  self.wait()                  
            else:
                 self.wait()
      def testexc(self,
                   canbox,
                   canchannel,
                   dbfile,                   
                   dictACFlg,
                   dictSigVal,
                   listmsgbox,
                   error):
            try:
                  mytest = TestSqe()
                  mytest.caninit(dbfile,canbox,canchannel,listmsgbox,error)
                  res=mytest.test()                  
                  self.result.emit(res)
                 
                  return True
            except Exception as e:
                  print(traceback.print_exc())
                  return False