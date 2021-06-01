# -*- coding: utf-8 -*-

#  debug.py
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
import traceback

from matrixrd import *
from signalbit import *
from mapread import mapread
from cantrx import cantrx
from signalbit import canconvert

def ACCreate(canbox,
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

if __name__ == "__main__":
    import time
    canbox = 'canalystii'
    dbfile = 'E:\\Project\\ProCCMTest\\ProCCMTest\\DBC\\M891改制冬标车版本_Body.dbc'
    flgacrun=1
    flagrun =None
    objectcantrx = None
    dictACFlg={'flgacon':0,
            'flgacauto':0,
            'flgacac':0,
            'flgacrec':0,
            'valacbl':1,
            'flgacdef':0,
            'flgacwindow':0,
            'flgacface':0,
            'flgacfoot':0,
            'valacltemp':22,
            'valacrtemp':22,
            'flgacdual':0,
            'flgacldef':0,
            'flgaclauto':0}
    dictSigVal = {'vspd':0,
                 'battcooltemp':0,
                 'battheattemp':0,
                 'ptcpwr':0,
                 'comppwr':0}

    flagrun,objectcantrx = ACCreate(canbox,dbfile,flgacrun,dictACFlg,dictSigVal)

    time.sleep(20)

    objectcantrx.stopsendperiod()

    
    
