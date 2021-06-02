# -*- coding: utf-8 -*-

#  cantxthread.py
#
#  ~~~~~~~~~~~~
#
#  Function CAN TX Thread
#
#  ~~~~~~~~~~~~
#
#  ------------------------------------------------------------------
#  Author : Li Yonghu
#  Build: 02.06.2021
#  Last change: 02.06.2021 Li Yonghu 
#
#  Language: Python 3.7
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


from cantrx import cantrx
from myctrlcan import myctrlcan



class RxThread(QThread):
      redict = Signal(dict)      
      
      def __init__(self,parent=None):
            super(RxThread,self).__init__(parent)           

            self.error = False
            self.completed = False
            
            #self.a2lpath=None      
            
      def init(self,
               mycantrx,
               dictACFlg):            

            self.mycantrx = mycantrx
            self.dictACFlg = dictACFlg                       

      def run(self):
            
            
            #while self.working ==True:
                  
            reflag,mysigdict=self.CANRxSig(self.mycantrx,
                                 self.dictACFlg)
            #print(mysigdict)
            
            #print 'cccc'
            if reflag == True:
                  self.redict.emit(mysigdict)                  
                  self.wait()
                  #self.finished.emit(self.completed)
            else:
                 self.wait()

            #self.result.emit(True)

      def CANRxSig(self,
                   mycantrx,
                   dictACFlg):
            #print('bbbb')
            try:
                   
                   mysiglist = mycantrx.initrxsig(dictACFlg)
##                   print('bbbb')
##                   print(mysiglist)
                   mysigdict = mycantrx.mymsgrecv(mysiglist)
##                   print('ccccc')
                  
                   return True,mysigdict           

            except Exception as e:
                  print(traceback.print_exc())
                  return False,None
