# -*- coding: utf-8 -*-

#  ctrlcantrx.py
#
#  ~~~~~~~~~~~~
#
#  Function Control CAN TX RX
#
#  ~~~~~~~~~~~~
#
#  ------------------------------------------------------------------
#  Author : Li Yonghu
#  Build: 28.05.2021
#  Last change: 28.05.2021 Li Yonghu 
#
#  Language: Python 3.7
#  ------------------------------------------------------------------
#  GNU GPL
#  
 
#

# Module Imports

import time
import os
import traceback

from matrixrd import *
from signalbit import *
from mapread import mapread
from cantrx import cantrx
from signalbit import canconvert

def ctrlcantrx(canbox,
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
