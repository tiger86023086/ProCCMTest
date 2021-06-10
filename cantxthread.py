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
class TxThread(QThread):
      msgbox = Signal(list)      
      
      def __init__(self,parent=None):
            super(TxThread,self).__init__(parent)           

            self.error = False
            self.completed = False
            
            #self.a2lpath=None      
            
      def init(self,
               mycantrx,
               dictACFlg,
               dictSigVal,
               listmsgbox):            

            self.mycantrx = mycantrx
            self.dictACFlg = dictACFlg
            self.dictSigVal = dictSigVal
            self.listmsgbox = listmsgbox           

      def run(self):                  
            reflag=self.CANTxSingel(self.mycantrx,
                                 self.dictACFlg,
                                 self.dictSigVal)
                  #self.sleep(5)
            #print 'cccc'
            if reflag == True:
                  #self.result.emit(True)                  
                  self.wait()
                  #self.finished.emit(self.completed)
            else:
                 self.wait()

            #self.result.emit(True)

      def CANTxSingel(self,
                      mycantrx,
                      dictACFlg,
                      dictSigVal):
            
            try:
                   mylistmsg,mymsgbox = mycantrx.inittxsig(dictACFlg,dictSigVal)                   
                  
                  #print('aaaaa')
                   for i in range(5):
                        #print('bbbbb') 
                        self.mycantrx.mymsgtx(mylistmsg)
                        time.sleep(0.004)
                   return True           

            except Exception as e:
                  print(traceback.print_exc())
                  mymsgbox = traceback.print_exc()
                  self.listmsgbox.append(mymsgbox)
                  return False