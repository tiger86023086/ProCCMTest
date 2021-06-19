# -*- coding: utf-8 -*-

#  MainTest.py
#
#  ~~~~~~~~~~~~
#
#  Function GUI MainWindow Thread
#
#  ~~~~~~~~~~~~
#
#  ------------------------------------------------------------------
#  Author : Li Yonghu
#  Build: 31.05.2021
#  Last change: 31.05.2021 Li Yonghu 
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

class myctrlcan:
    def __init__(self,dbfile,canbox,canchannel,listmsgbox,error,mylogger):
        self.channel = 0
        self.listmsgbox = listmsgbox
        self.error = error
        self.mylogger = mylogger
        try:
            self.mapdict = mapread('map.xls',self.listmsgbox)
        except Exception as e:
              self.error = True                  
              mymsgbox = traceback.print_exc()
              print(mymsgbox)
              self.listmsgbox.append(mymsgbox)
              self.mylogger.error(mymsgbox)
        try: 
            if dbfile != None:
                self.mycanconv = canconvert()
                self.mycanconv.initcandb(dbfile)
                mymsgbox = 'The dbc has been install --'+dbfile
                print(mymsgbox)
                self.listmsgbox.append(mymsgbox)
                self.mylogger.info(mymsgbox)
            else:
                self.error = True
                mymsgbox = 'The dbc is none'
                print(mymsgbox)
                self.listmsgbox.append(mymsgbox)
                self.mylogger.war(mymsgbox)
        except Exception as e:
              self.error = True                  
              mymsgbox = traceback.print_exc()
              print(mymsgbox)
              self.listmsgbox.append(mymsgbox)
              self.mylogger.error(mymsgbox)

        self.mycantrx = cantrx()
                            
        if canbox == 'canalystii':
            try:
                if canchannel != None:
                    self.channel = eval(canchannel)
                    print(canchannel)
                    res = self.mycantrx.initcan(canbox,self.channel,500000)
                    if res:
                        mymsgbox = 'You slecet canbox--canalystii(chuangxin)'
                        print(mymsgbox)
                        self.listmsgbox.append(mymsgbox)
                        self.mylogger.info(mymsgbox)                    
                    else:
                        mymsgbox = 'You cannot initialize canalystii(chuangxin)'
                        print(mymsgbox)
                        self.listmsgbox.append(mymsgbox)
                        self.mylogger.info(mymsgbox)
                    
            except Exception as e:
              self.error = True                  
              mymsgbox = traceback.print_exc()
              print(mymsgbox)
              self.listmsgbox.append(mymsgbox)
              self.mylogger.error(mymsgbox)
        elif canbox == 'kvaser':
            try:
                if canchannel != None:
                    self.channel = eval(canchannel)
                    res = self.mycantrx.initcan(canbox,self.channel,500000)
                    if res:
                        mymsgbox = 'You slecet canbox--kavaser'
                        print(mymsgbox)
                        self.listmsgbox.append(mymsgbox)
                        self.mylogger.info(mymsgbox)                    
                    else:
                        mymsgbox = 'You cannot initialize kavaser'
                        print(mymsgbox)
                        self.listmsgbox.append(mymsgbox)
                        self.mylogger.info(mymsgbox)
                    
            except Exception as e:
              self.error = True                  
              mymsgbox = traceback.print_exc()
              print(mymsgbox)
              self.listmsgbox.append(mymsgbox)
              self.mylogger.error(mymsgbox)
        elif canbox == 'pcan':
            try:
                if canchannel != None:
                    res = self.mycantrx.initcan(canbox,canchannel,500000)
                    if res:
                        mymsgbox = 'You slecet canbox--PCAN'
                        print(mymsgbox)
                        self.listmsgbox.append(mymsgbox)
                        self.mylogger.info(mymsgbox)                        
                    else:
                        mymsgbox = 'You cannot initialize kavaser'
                        print(mymsgbox)
                        self.listmsgbox.append(mymsgbox)
                        self.mylogger.info(mymsgbox)
                    if canchannel == 'PCANUSB1':
                        self.channel = 0
                    elif canchannel == 'PCANUSB2':
                        self.channel = 1
                    elif canchannel == 'PCANUSB3':
                        self.channel = 2
                    elif canchannel == 'PCANUSB4':
                        self.channel = 3
                    else:
                        self.channel = 0
                    
            except Exception as e:
              self.error = True                  
              mymsgbox = traceback.print_exc()
              print(mymsgbox)
              self.listmsgbox.append(mymsgbox)
              self.mylogger.error(mymsgbox)
        elif canbox == 'neovi':
            try:
                if canchannel != None:
                    self.channel = eval(canchannel)
                    res = self.mycantrx.initcan(canbox,self.channel,500000)
                    if res:
                        mymsgbox = 'You slecet canbox--neoVI'
                        print(mymsgbox)
                        self.listmsgbox.append(mymsgbox)
                        self.mylogger.info(mymsgbox)                    
                    else:
                        mymsgbox = 'You cannot initialize neoVI'
                        print(mymsgbox)
                        self.listmsgbox.append(mymsgbox)
                        self.mylogger.info(mymsgbox)
                    
            except Exception as e:
              self.error = True                  
              mymsgbox = traceback.print_exc()
              print(mymsgbox)
              self.listmsgbox.append(mymsgbox)
              self.mylogger.error(mymsgbox)
        else:
            self.error = True
            mymsgbox = 'You select null canbox!'
            print(mymsgbox)
            self.listmsgbox.append(mymsgbox)
            self.mylogger.info(mymsgbox)

    def inittxsig(self,dictACFlg,dictSigVal):

        dictsig = {}
        iterdictac = iter(dictACFlg)

        while True:
              try:
                    dictkey = next(iterdictac)
                    [CANsigTx,CANsigRx]= self.mapdict[dictkey]
                    CANsigTxVal = dictACFlg[dictkey]
                    dictsig[CANsigTx] = CANsigTxVal                    
              except StopIteration:
                    break       

        iterdictsig = iter(dictSigVal)
        
        while True:
              try:
                    dictkey = next(iterdictsig)
                    [CANsigTx,CANsigRx]= self.mapdict[dictkey]
                    CANsigTxVal = dictSigVal[dictkey]
                    dictsig[CANsigTx] = CANsigTxVal
              except StopIteration:
                    break        
        try:
            mysigdata,myid  = self.mycanconv.encodemsg(dictsig)
            mylistmsg = self.mycantrx.clustermsg(mysigdata,myid,self.channel)
        except Exception as e:
              self.error = True                  
              mymsgbox = traceback.print_exc()
              print(mymsgbox)
              self.listmsgbox.append(mymsgbox)
              self.mylogger.error(mymsgbox)
        

        mymsgbox = 'Master send messages'
        print(mymsgbox)
        self.mylogger.info(mymsgbox)
        #self.listmsgbox.append(mymsgbox)

        return mylistmsg,self.listmsgbox
    def initrxsig(self,dictACFlg):
        mysiglist = list()
        iterdictac = iter(dictACFlg)
        while True:
              try:
                    dictkey = next(iterdictac)
                    [CANsigTx,CANsigRx]= self.mapdict[dictkey]                    

                    if CANsigRx != '':
                        mysiglist.append(CANsigRx)
              except StopIteration:
                    break

        mymsgbox = 'Master recieve messages '
        print(mymsgbox)
        self.mylogger.info(mymsgbox)
        #self.listmsgbox.append(mymsgbox)
        return mysiglist,self.listmsgbox

    def mymsgtxperiod(self,mylistmsg):        
        for msg in mylistmsg:
            mymsg = msg[0]
          #print(type(mymsg))
            mycycle = float(msg[1]/1000)
          #print(type(mycycle))
            #tasks[mymsg] = mycantrx.sendmsgperiod(mymsg,mycycle)
            self.mycantrx.sendmsgperiod(mymsg,mycycle)

    def mymsgtx(self,mylistmsg):

        for msg in mylistmsg:
            mymsg = msg[0]            
          #print(type(mymsg))
            #mycycle = float(msg[1]/1000)
          #print(type(mycycle))
            #tasks[mymsg] = mycantrx.sendmsgperiod(mymsg,mycycle)
            self.mycantrx.sendmsg(mymsg)

    def mymsgstop(self):
        self.mycantrx.stopsendperiod()

    def mymsgrecv(self,mysiglist):

        mysigdict = dict()
        mylistid = self.mycanconv.idserach(mysiglist)
        #print(mylistid)
        for i in range(len(mylistid)):
            while True:                               
                try:
                    canrecvmsg = self.mycantrx.recvmsg()
                    #print(canrecvmsg)
                    #print(mylistid[i])
                    if canrecvmsg != None:
                        if canrecvmsg.arbitration_id == mylistid[i] :
                            dicttemp = self.mycanconv.decodemsg(canrecvmsg.arbitration_id,
                                                    canrecvmsg.data)
                            mysigdict.update(dicttemp)
                            break
                except Exception as e:
                    mymsgbox = traceback.print_exc()
                    print(mymsgbox)
                    self.mylogger.error(mymsgbox)
                    time.sleep(0.001)
                    #self.listmsgbox.append('waitting receive rxmessage')  
                    
            #time.sleep(0.5)
        return mysigdict
    def mydelcan(self):
        self.mycantrx.delcan()

if __name__ == "__main__":
    import time
    import logging
    from mylog import Logger
    mylogger = Logger('mylog.log',logging.ERROR,logging.DEBUG)
    canbox = 'canalystii'
    dbfile = 'E:\\Project\\ProCCMTest\\ProCCMTest\\code\\DBC\\6.0\\MAS891A_VehicleBody_Matrix_V6.0_for_B5_R0.5.0 - CCM.dbc'
    channel = '0'
    listmsgbox = list()
    myerror = False
    flgacrun=1
    flagrun =None
    objectcantrx = None
    dictACFlg={'flgacon':3,
                'flgacauto':3,
                'flgacac':2,
                'flgacrec':3,
                'valacbl':7,
                'flgacdef':3,
                'flgacmode':7,                            
                'valacltemp':47.5,
                 'valacrtemp':47.5,
                 'flgacdual':3,
                'valacblT':7,
                'valacltempT':47.5,
                'valacrtempT':47.5,
                'flgbcmon':3}
    dictSigVal = {'vspd':0,
                 'battcooltemp':0,
                 'battheattemp':0,
                 'ptcpwr':0,
                 'comppwr':0}

    mycan = myctrlcan(dbfile,canbox,channel,listmsgbox,myerror,mylogger)
    mylistmsg,msgbox = mycan.inittxsig(dictACFlg,dictSigVal)
    #mysiglist,msgbox = mycan.initrxsig(dictACFlg)
    mycan.mymsgtxperiod(mylistmsg)
    time.sleep(10)

    # dictACFlg={'flgacon':3,
    #             'flgacauto':1,
    #             'flgacac':2,
    #             'flgacrec':3,
    #             'valacbl':7,
    #             'flgacdef':3,
    #             'flgacmode':7,                            
    #             'valacltemp':47.5,
    #              'valacrtemp':47.5,
    #              'flgacdual':3,
    #             'valacblT':7,
    #             'valacltempT':47.5,
    #             'valacrtempT':47.5,
    #             'flgbcmon':3}

    # mylistmsg,msgbox= mycan.inittxsig(dictACFlg,dictSigVal)
    # for i in range(5):        
    #     mycan.mymsgtx(mylistmsg)
    #     time.sleep(0.004)
    
    # print(mysiglist)
    # mysigdict = mycan.mymsgrecv(mysiglist)
    # print('aaaaaaaa')
    # print(mysigdict)
    # print('bbbbbbb')
    # time.sleep(20)
    mycan.mymsgstop()

    mycan.mydelcan
