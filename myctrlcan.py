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
    def __init__(self,dbfile,canbox):
        
        listmsgbox = ''
        self.mapdict = mapread('map.xls',listmsgbox)
        if dbfile != '':
              self.mycanconv = canconvert()
              self.mycanconv.initcandb(dbfile)
              mymsgbox = 'The dbc has been install --'+dbfile
              print(mymsgbox)
        else:
            mymsgbox = 'The dbc is none'
            print(mymsgbox)

        self.mycantrx = cantrx()
                            
        if canbox == 'canalystii':
            self.mycantrx.initcan(canbox,0,500000)
            mymsgbox = 'You slecet canbox--canalystii(chuangxin)'
            print(mymsgbox)
        else:
            mymsgbox = 'You select null canbox!'
            print(mymsgbox)

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

        mysigdata,myid  = self.mycanconv.encodemsg(dictsig)
        mylistmsg = self.mycantrx.clustermsg(mysigdata,myid)

        return mylistmsg
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
        return mysiglist

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

        for i in range(len(mylistid)):
            canrecvmsg = self.mycantrx.recvmsg()
##            print(canrecvmsg.arbitration_id)
##            print(mylistid[i])
            if canrecvmsg.arbitration_id in mylistid :
                dicttemp = self.mycanconv.decodemsg(canrecvmsg.arbitration_id,
                                           canrecvmsg.data)
                mysigdict.update(dicttemp)
                print('qqqq')
        return mysigdict
    def mydelcan(self):
        self.mycantrx.delcan()

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

    mycan = myctrlcan(dbfile,canbox)
    mylistmsg = mycan.inittxsig(dictACFlg,dictSigVal)
    mysiglist = mycan.initrxsig(dictACFlg)
    mycan.mymsgtxperiod(mylistmsg)

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
            'flgaclauto':1}

    mylistmsg = mycan.inittxsig(dictACFlg,dictSigVal)
    for i in range(5):        
        mycan.mymsgtx(mylistmsg)
        time.sleep(0.004)
    
    print(mysiglist)
    mysigdict = mycan.mymsgrecv(mysiglist)
    print('aaaaaaaa')
    print(mysigdict)
    print('bbbbbbb')

    
    
    

    time.sleep(60)
    mycan.mymsgstop()

    mycan.mydelcan
