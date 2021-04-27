# -*- coding: utf-8 -*-

#  acthread.py
#
#  ~~~~~~~~~~~~
#
#  Function GUI AC Thread
#
#  ~~~~~~~~~~~~
#
#  ------------------------------------------------------------------
#  Author : Li Yonghu
#  Build: 24.04.2021
#  Last change: 26.04.2021 Li Yonghu 
#
#  Language: Python 3.7  PyQt5.15.2
#  ------------------------------------------------------------------
#  GNU GPL
#  
 
#

# Module Imports

from PyQt5.QtCore import (Qt,QThread,QMutex)
from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtCore import pyqtSlot as Slot
import time,os


from matrixrd import *
from signalbit import *
from mapread import mapread
from cantrx import cantrx
from signalbit import canconvert



class ACThread(QThread):
      
      def __init__(self,parent=None):
            super(ACThread,self).__init__(parent)

            self.error = False
            self.completed = False
            
            #self.a2lpath=None
      def initialize(self,canbox,dbfile,
                     flgacrun,flgsigrun,
                     dictACFlg,dictSigVal,
                     listmessagebox):            

            self.canbox = canbox
            self.dbfile = dbfile
            self.flgacrun = flgacrun
            self.flgsigrun = flgsigrun
            self.dictACFlg = dictACFlg
            self.dictSigVal = dictSigVal
            self.listmessagebox = listmessagebox      

      def run(self):
            
            #print 'bbbb'
            reflag=self.ACCreate(self.canbox,
                                 self.dbfile,
                                 self.flgacrun,
                                 self.flgsigrun,
                                 self.dictACFlg,
                                 self.dictSigVal)
            #print 'cccc'
            if reflag == True:
                  self.wait()
                  self.finished.emit(self.completed)
            else:
                 self.wait() 


      def ACCreate(self,canbox,dbfile,
                   flgacrun,flgsigrun,
                   dictACFlg,dictSigVal,
                   listmessagebox):
            
            mapdict = mapread('map.xls',listmessagebox)
            dictsig = {}
            mycanconv = canconvert.initcandb(dbfile)

            tasks={}
            
            try:
                  iterdictac = iter(dictACFlg)
                  if flgacrun:
                      while True:
                            try:
                                  dictkey = next(iterdictac)
                                  [CANsigTx,CANsigRx]= mapdict[dictkey]
                                  CANsigTxVal = dictACFlg[dictkey]
                                  dictsig[CANsigTx] = CANsigTxVal
                            except StopIteration:
                                  break                                  
                                  
                      if canbox == 'canalystii':
                            mycantrx = cantrx.initcan(canbox,0,500000)
                            mysigdata,myid  = mycan.encodemsg(dictsig)
                            mylistmsg = mycantrx.clustermsg(mysigdata,myid)
                            tasks={}
                            for msg in mylistmsg:
        
                                mymsg = msg[0]
                                print(type(mymsg))
                                mycycle = float(msg[1]/1000)
                                print(type(mycycle))
                                tasks[mymsg] = mycantrx.sendmsgperiod(mymsg,mycycle)
                                #counter =counter + 1
                                print(tasks)

                  else:
                        if len(list(tasks.keys())) != 0:
                              if canbox == 'canalystii':
                                    for tkey in list(tasks.keys()):
                                          tasks[tkey].stop()
                              else:
                                    pass
            except:
                  print('In AC Thread,There is some error!')
