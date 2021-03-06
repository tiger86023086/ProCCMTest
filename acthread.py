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
#  Last change: 12.05.2021 Li Yonghu 
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


from matrixrd import *
from signalbit import *
from mapread import mapread
from cantrx import cantrx
from signalbit import canconvert



class ACThread(QThread):
      result = Signal(bool)
      cantrx = Signal(object)
      
      def __init__(self,parent=None):
            super(ACThread,self).__init__(parent)           

            self.error = False
            self.completed = False
            
            #self.a2lpath=None      
            
      def initialize(self,
                     canbox,
                     dbfile,
                     flgacrun,
                     dictACFlg,
                     dictSigVal):            

            self.canbox = canbox
            self.dbfile = dbfile
            self.flgacrun = flgacrun
            #self.flgsigrun = flgsigrun
            self.dictACFlg = dictACFlg
            self.dictSigVal = dictSigVal
            #self.listmessagebox = listmessagebox
            

      def run(self):
            
            #print 'bbbb'
            #while self.working ==True:
                  
            reflag,mycantrx=self.ACCreate(self.canbox,
                                 self.dbfile,
                                 self.flgacrun,
                                 self.dictACFlg,
                                 self.dictSigVal)
                  #self.sleep(5)
            #print 'cccc'
            if reflag == True:
                  self.result.emit(True)
                  self.cantrx.emit(mycantrx)
                  #self.wait()
                  #self.finished.emit(self.completed)
            else:
                 self.wait()

            #self.result.emit(True)

      def ACCreate(self,
                   canbox,
                   dbfile,
                   flgacrun,
                   dictACFlg,
                   dictSigVal):
            try:
                    listmessagebox = ''#temporary
        
                    mapdict = mapread('map.xls',listmessagebox)
                    dictsig = {}
                    if dbfile != '':
                          mycanconv = canconvert()
                          mycanconv.initcandb(dbfile)

                          tasks={}
                          
                          try:
                                
                                if flgacrun:

                                    iterdictac = iter(dictACFlg)
                                    
                                    while True:
                                          try:
                                                dictkey = next(iterdictac)
                                                [CANsigTx,CANsigRx]= mapdict[dictkey]
                                                CANsigTxVal = dictACFlg[dictkey]
                                                dictsig[CANsigTx] = CANsigTxVal
                                          except StopIteration:
                                                break

                                    iterdictsig = iter(dictSigVal)
                                    
                                    while True:
                                          try:
                                                dictkey = next(iterdictsig)
                                                [CANsigTx,CANsigRx]= mapdict[dictkey]
                                                CANsigTxVal = dictSigVal[dictkey]
                                                dictsig[CANsigTx] = CANsigTxVal
                                          except StopIteration:
                                                break

                                            
                                    mysigdata,myid  = mycanconv.encodemsg(dictsig)

                                    mycantrx = cantrx()

                                    mylistmsg = mycantrx.clustermsg(mysigdata,myid)
                                                
                                    if canbox == 'canalystii':
                                          mycantrx.initcan(canbox,0,500000)                             
                                          
                                          tasks={}
                                          for msg in mylistmsg:
                      
                                              mymsg = msg[0]
                                              #print(type(mymsg))
                                              mycycle = float(msg[1]/1000)
                                              #print(type(mycycle))
                                              tasks[mymsg] = mycantrx.sendmsgperiod(mymsg,mycycle)
                                              #counter =counter + 1
                                              #print(tasks)
                                    print('acthread true end')

                                else:

                                    iterdictac = iter(dictACFlg)
                                    
                                    while True:
                                          try:
                                                dictkey = next(iterdictac)
                                                [CANsigTx,CANsigRx]= mapdict[dictkey]
                                                CANsigTxVal = dictACFlg[dictkey]
                                                dictsig[CANsigTx] = CANsigTxVal
                                          except StopIteration:
                                                break

                                    iterdictsig = iter(dictSigVal)
                                    
                                    while True:
                                          try:
                                                dictkey = next(iterdictsig)
                                                [CANsigTx,CANsigRx]= mapdict[dictkey]
                                                CANsigTxVal = dictSigVal[dictkey]
                                                dictsig[CANsigTx] = CANsigTxVal
                                          except StopIteration:
                                                break

                                            
                                    mysigdata,myid  = mycanconv.encodemsg(dictsig)

                                    mycantrx = cantrx()

                                    mylistmsg = mycantrx.clustermsg(mysigdata,myid)
                                                
                                    if canbox == 'canalystii':
                                          mycantrx.initcan(canbox,0,500000)                             
                                          
                                          tasks={}
                                          for msg in mylistmsg:
                      
                                              mymsg = msg[0]
                                              #print(type(mymsg))
                                              mycycle = float(msg[1]/1000)
                                              #print(type(mycycle))
                                              tasks[mymsg] = mycantrx.sendmsgperiod(mymsg,mycycle)
                                              #counter =counter + 1
                                              #print(tasks)
                                      
                                
                                    try:
                                        if isinstance(mycantrx,cantrx):
                                            mycantrx.stopsendperiod()
                                            print('mycantrx')
                                            
                                        else:
                                            pass
                                    except:
                                        pass

##                                    print('111111')
##                                    print(len(list(tasks.keys())))
##                                    if len(list(tasks.keys())) != 0:
##                                          if canbox == 'canalystii':
##                                                for tkey in list(tasks.keys()):
##                                                      tasks[tkey].stop()
##                                          else:
##                                                pass
                                          
                                print('acthread false end')
                              
                                return True,mycantrx
                          except Exception as e:
                                print('In AC Thread,There is some error!')
                                print(traceback.print_exc())
                                return False,None

                    else:
                          print('There is no dbc!')
                          return False,None

            except Exception as e:
                  print(traceback.print_exc())
                  return False,None
