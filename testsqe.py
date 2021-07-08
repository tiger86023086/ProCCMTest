# -*- coding: utf-8 -*-

#  testsqe.py
#
#  ~~~~~~~~~~~~
#
#  Function GUI Test Sequence
#
#  ~~~~~~~~~~~~
#
#  ------------------------------------------------------------------
#  Author : Li Yonghu
#  Build: 23.06.2021
#  Last change: 23.06.2021 Li Yonghu 
#
#  Language: Python 3.7
#  ------------------------------------------------------------------
#  GNU GPL
#  
 
#

# Module Imports

from myctrlcan import myctrlcan
import time,os
from mylog import Logger
from myctrlcan import myctrlcan

TsON = 1
TsOFF = 0
TsAUTOON = 1
TsAUTOOFF = 0
TsACON = 1
TsACOFF = 0
TsREC = 0
TsFRE = 1
TsSYNON = 0
TsSYNOFF = 1
TsFace = 0
TsFaFt = 1
TsFt = 2
TsFtWin = 3
TsWIN = 4
TsDEFON = 1
TsDEFOFF = 0

class TestSqe():

      def __init__(self):
        self.initacsig()
        self.initsigval()        
        self.mylogger = Logger('actest.log')
        self.tsresult = True
        self.mycantrx = None
      def initacsig(self):
            self.dictACFlg={'flgacon':3,
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
      def initsigval(self):
            self.dictSigVal={'vspd':0,
                             'battcooltemp':0,
                             'battheattemp':0,
                             'ptcpwr':0,
                             'comppwr':0}
      def caninit(self,dbfile,canbox,canchannel,listmsgbox,error):
        self.mycantrx = myctrlcan(dbfile,canbox,canchannel,listmsgbox,error,self.mylogger)
        mylistmsg,msgbox= self.mycantrx.inittxsig(self.dictACFlg,self.dictSigVal)                  
        self.mycantrx.mymsgtxperiod(mylistmsg)
        time.sleep(5)        

      def test(self,progressVal):
          self.mylogger.info('-----------$$$$$$$$$$$------------')
          self.test1()
          progressVal[0] = 12.5
          self.test2()
          progressVal[0] = progressVal+12.5
          self.test3()
          progressVal[0] = progressVal+12.5
          self.test4()
          progressVal[0] = progressVal+12.5
          self.test5()
          progressVal[0] = progressVal+12.5
          self.test6()
          progressVal[0] = progressVal+12.5
          self.test7()
          progressVal[0] = progressVal+12.5
          self.test8()
          progressVal[0] = progressVal+12.5
          self.mylogger.info('-----------#############------------')
          self.mycantrx.mymsgstop()
          self.mycantrx.mydelcan()
          return self.tsresult
         
      def test1(self):
             #test1
          self.mylogger.info('-----------test1------------')
          self.dictACFlg['flgacon'] = TsON
          mylistmsg,msgbox= self.mycantrx.inittxsig(self.dictACFlg,self.dictSigVal)
          for i in range(5):
              self.mycantrx.mymsgtx(mylistmsg)
              time.sleep(0.004)
          self.mylogger.info('test1 ONOFF test')

          time.sleep(5)
          mysiglist,msgbox = self.mycantrx.initrxsig(self.dictACFlg)
          for i in range(30):
              mysigdict = self.mycantrx.mymsgrecv(mysiglist)
              time.sleep(0.1)
          print(mysigdict)
          if mysigdict['CCM_Off'] == 1:
              self.mylogger.info('test1 Pass:CCM_Off=1')
          elif mysigdict['CCM_Off'] == 0:
             self.mylogger.info('test1 Fail:CCM_Off=0')
             self.tsresult = False
          else:
              self.mylogger.info('test1 Fail:CCM_Off=None')
              self.tsresult = False

          self.dictACFlg['flgacon'] = TsOFF
          mylistmsg,msgbox= self.mycantrx.inittxsig(self.dictACFlg,self.dictSigVal)
          for i in range(5):
              self.mycantrx.mymsgtx(mylistmsg)
              time.sleep(0.004)

          time.sleep(5)
          mysiglist,msgbox = self.mycantrx.initrxsig(self.dictACFlg)
          for i in range(30):
              mysigdict = self.mycantrx.mymsgrecv(mysiglist)
              time.sleep(0.1)
          print(mysigdict)
          if mysigdict['CCM_Off'] == 0:
              self.mylogger.info('test1 Pass:CCM_Off=0')
          elif mysigdict['CCM_Off'] == 1:
             self.mylogger.info('test1 Fail:CCM_Off=1')
             self.tsresult = False
          else:
              self.mylogger.info('test1 Fail:CCM_Off=None')
              self.tsresult = False
          self.mylogger.info('------------test1 over----------------')
          self.initacsig()

      def test2(self):
             #test2
          self.mylogger.info('------------------test2---------------')
          self.dictACFlg['flgacauto'] = TsAUTOON
          mylistmsg,msgbox= self.mycantrx.inittxsig(self.dictACFlg,self.dictSigVal)
          for i in range(5):
              self.mycantrx.mymsgtx(mylistmsg)
              time.sleep(0.004)
          self.mylogger.info('test2 AutoONOFF test')

          time.sleep(5)
          mysiglist,msgbox = self.mycantrx.initrxsig(self.dictACFlg)
          for i in range(30):
              mysigdict = self.mycantrx.mymsgrecv(mysiglist)
              time.sleep(0.1)

          if mysigdict['CCM_AUTOSts'] == 1:
              self.mylogger.info('test2 Pass:CCM_AUTOSts=1')
          elif mysigdict['CCM_AUTOSts'] == 0:
             self.mylogger.info('test2 Fail:CCM_AUTOSts=0')
             self.tsresult = False
          else:
              self.mylogger.info('test2 Fail:CCM_AUTOSts=None')
              self.tsresult = False

          self.dictACFlg['flgacauto'] = TsAUTOOFF
          mylistmsg,msgbox= self.mycantrx.inittxsig(self.dictACFlg,self.dictSigVal)
          for i in range(5):
              self.mycantrx.mymsgtx(mylistmsg)
              time.sleep(0.004)

          time.sleep(5)
          mysiglist,msgbox = self.mycantrx.initrxsig(self.dictACFlg)
          for i in range(30):
              mysigdict = self.mycantrx.mymsgrecv(mysiglist)
              time.sleep(0.1)

          if mysigdict['CCM_AUTOSts'] == 1:
              self.mylogger.info('test2 Pass:CCM_AUTOSts=1')
          elif mysigdict['CCM_AUTOSts'] == 0:
             self.mylogger.info('test2 Fail:CCM_AUTOSts=0')
             self.tsresult = False
          else:
              self.mylogger.info('test2 Fail:CCM_AUTOSts=None')
              self.tsresult = False
          self.mylogger.info('-------------------test2 over--------------')
          self.initacsig()

      def test3(self):
             #test3
          self.mylogger.info('-------------test3-----------------')
          self.dictACFlg['flgacac'] = TsACON
          mylistmsg,msgbox= self.mycantrx.inittxsig(self.dictACFlg,self.dictSigVal)
          for i in range(5):
              self.mycantrx.mymsgtx(mylistmsg)
              time.sleep(0.004)
          self.mylogger.info('test3 ACONOFF test')

          time.sleep(5)
          mysiglist,msgbox = self.mycantrx.initrxsig(self.dictACFlg)
          for i in range(30):
              mysigdict = self.mycantrx.mymsgrecv(mysiglist)
              time.sleep(0.1)

          if mysigdict['CCM_ACSts'] == 1:
              self.mylogger.info('test3 Pass:CCM_ACSts=1')
          elif mysigdict['CCM_ACSts'] == 0:
             self.mylogger.info('test3 Fail:CCM_ACSts=0')
             self.tsresult = False
          else:
              self.mylogger.info('test3 Fail:CCM_ACSts=None')
              self.tsresult = False

          self.dictACFlg['flgacac'] = TsACOFF
          mylistmsg,msgbox= self.mycantrx.inittxsig(self.dictACFlg,self.dictSigVal)
          for i in range(5):
              self.mycantrx.mymsgtx(mylistmsg)
              time.sleep(0.004)

          time.sleep(5)
          mysiglist,msgbox = self.mycantrx.initrxsig(self.dictACFlg)
          for i in range(30):
              mysigdict = self.mycantrx.mymsgrecv(mysiglist)
              time.sleep(0.1)

          if mysigdict['CCM_ACSts'] == 0:
              self.mylogger.info('test3 Pass:CCM_ACSts=1')
          elif mysigdict['CCM_ACSts'] == 1:
             self.mylogger.info('test3 Fail:CCM_ACSts=0')
             self.tsresult = False
          else:
              self.mylogger.info('test3 Fail:CCM_ACSts=None')
              self.tsresult = False
          self.mylogger.info('---------test3 over--------')
      def test4(self):
             #test4
          self.mylogger.info('------------test4 RECONOFF test---------------')
          self.mylogger.info('test4')
          self.dictACFlg['flgacrec'] = TsREC
          mylistmsg,msgbox= self.mycantrx.inittxsig(self.dictACFlg,self.dictSigVal)
          for i in range(5):
              self.mycantrx.mymsgtx(mylistmsg)
              time.sleep(0.004)          

          time.sleep(1)
          mysiglist,msgbox = self.mycantrx.initrxsig(self.dictACFlg)
          for i in range(30):
              mysigdict = self.mycantrx.mymsgrecv(mysiglist)
              time.sleep(0.1)

          if mysigdict['CCM_CycleStatus'] == 0:
              self.mylogger.info('test2 Pass:CCM_CycleStatus=0')
          elif mysigdict['CCM_CycleStatus'] == 1:
             self.mylogger.info('test2 Fail:CCM_CycleStatus=1')
             self.tsresult = False
          else:
              self.mylogger.info('test2 Fail:CCM_CycleStatus=None')
              self.tsresult = False

          self.dictACFlg['flgacrec'] = TsFRE
          mylistmsg,msgbox= self.mycantrx.inittxsig(self.dictACFlg,self.dictSigVal)
          for i in range(5):
              self.mycantrx.mymsgtx(mylistmsg)
              time.sleep(0.004)

          time.sleep(5)
          mysiglist,msgbox = self.mycantrx.initrxsig(self.dictACFlg)
          for i in range(30):
              mysigdict = self.mycantrx.mymsgrecv(mysiglist)
              time.sleep(0.1)

          if mysigdict['CCM_CycleStatus'] == 1:
              self.mylogger.info('test4 Pass:CCM_CycleStatus=1')
          elif mysigdict['CCM_CycleStatus'] == 0:
             self.mylogger.info('test4 Fail:CCM_CycleStatus=0')
             self.tsresult = False
          else:
              self.mylogger.info('test4 Fail:CCM_CycleStatus=None')
              self.tsresult = False
          self.mylogger.info('-----------test4 over----------')

      def test5(self):
             #test5
          self.mylogger.info('------------test5 DEFONOFF test---------------')
          self.mylogger.info('test5')
          self.dictACFlg['flgacdef'] = TsDEFON
          mylistmsg,msgbox= self.mycantrx.inittxsig(self.dictACFlg,self.dictSigVal)
          for i in range(5):
              self.mycantrx.mymsgtx(mylistmsg)
              time.sleep(0.004)          

          time.sleep(1)
          mysiglist,msgbox = self.mycantrx.initrxsig(self.dictACFlg)
          for i in range(30):
              mysigdict = self.mycantrx.mymsgrecv(mysiglist)
              time.sleep(0.1)

          if mysigdict['CCM_FrontDefrostSts'] == 1:
              self.mylogger.info('test5 Pass:CCM_FrontDefrostSts=0')
          elif mysigdict['CCM_FrontDefrostSts'] == 0:
             self.mylogger.info('test5 Fail:CCM_FrontDefrostSts=1')
             self.tsresult = False
          else:
              self.mylogger.info('test5 Fail:CCM_FrontDefrostSts=None')
              self.tsresult = False

          self.dictACFlg['flgacdef'] = TsDEFOFF
          mylistmsg,msgbox= self.mycantrx.inittxsig(self.dictACFlg,self.dictSigVal)
          for i in range(5):
              self.mycantrx.mymsgtx(mylistmsg)
              time.sleep(0.004)

          time.sleep(5)
          mysiglist,msgbox = self.mycantrx.initrxsig(self.dictACFlg)
          for i in range(30):
              mysigdict = self.mycantrx.mymsgrecv(mysiglist)
              time.sleep(0.1)

          if mysigdict['CCM_FrontDefrostSts'] == 0:
              self.mylogger.info('test5 Pass:CCM_FrontDefrostSts=0')
          elif mysigdict['CCM_FrontDefrostSts'] == 1:
             self.mylogger.info('test5 Fail:CCM_FrontDefrostSts=1')
             self.tsresult = False
          else:
              self.mylogger.info('test5 Fail:CCM_CycleStatus=None')
              self.tsresult = False
          self.mylogger.info('-----------test5 over----------')   
    
      def test6(self):
             #test6
          self.mylogger.info('------------test6 Blower Level test---------------')
          self.mylogger.info('test6')
          self.dictACFlg['valacbl'] = 5
          mylistmsg,msgbox= self.mycantrx.inittxsig(self.dictACFlg,self.dictSigVal)
          for i in range(5):
              self.mycantrx.mymsgtx(mylistmsg)
              time.sleep(0.004)          

          time.sleep(1)
          mysiglist,msgbox = self.mycantrx.initrxsig(self.dictACFlg)
          for i in range(30):
              mysigdict = self.mycantrx.mymsgrecv(mysiglist)
              time.sleep(0.1)

          if mysigdict['CCM_FanGearDisplay'] == 5:
              self.mylogger.info('test6 Pass:CCM_FanGearDisplay=5')          
          else:
              self.mylogger.info('test6 Fail')
              self.tsresult = False

          self.dictACFlg['valacbl'] = 1
          mylistmsg,msgbox= self.mycantrx.inittxsig(self.dictACFlg,self.dictSigVal)
          for i in range(5):
              self.mycantrx.mymsgtx(mylistmsg)
              time.sleep(0.004)

          time.sleep(5)
          mysiglist,msgbox = self.mycantrx.initrxsig(self.dictACFlg)
          for i in range(30):
              mysigdict = self.mycantrx.mymsgrecv(mysiglist)
              time.sleep(0.1)

          if mysigdict['CCM_FanGearDisplay'] == 1:
              self.mylogger.info('test6 Pass:CCM_FanGearDisplay=1')
         
          else:
              self.mylogger.info('test6 Fail')
              self.tsresult = False
          self.mylogger.info('-----------test6 over----------')

      def test7(self):
             #test7
          self.mylogger.info('------------test7 Tempature test---------------')
          self.mylogger.info('test7')
          self.dictACFlg['flgacon'] = TsON
          mylistmsg,msgbox= self.mycantrx.inittxsig(self.dictACFlg,self.dictSigVal)
          for i in range(5):
              self.mycantrx.mymsgtx(mylistmsg)
              time.sleep(0.004)
          time.sleep(5)
          
          self.dictACFlg['valacltemp'] = 22
          self.dictACFlg['valacrtemp'] = 25
          mylistmsg,msgbox= self.mycantrx.inittxsig(self.dictACFlg,self.dictSigVal)
          for i in range(5):
              self.mycantrx.mymsgtx(mylistmsg)
              time.sleep(0.004)
          time.sleep(5)

          mysiglist,msgbox = self.mycantrx.initrxsig(self.dictACFlg)
          for i in range(30):
              mysigdict = self.mycantrx.mymsgrecv(mysiglist)
              time.sleep(0.1)

          if int(mysigdict['CCM_FLTempSts']) == 22 and int(mysigdict['CCM_FRTempSts']) == 25:
              self.mylogger.info('test7 Pass')          
          else:
              self.mylogger.info('test7 Fail')
              self.tsresult = False

          self.dictACFlg['valacltemp'] = 16
          self.dictACFlg['valacrtemp'] = 22
          mylistmsg,msgbox= self.mycantrx.inittxsig(self.dictACFlg,self.dictSigVal)
          for i in range(5):
              self.mycantrx.mymsgtx(mylistmsg)
              time.sleep(0.004)

          time.sleep(5)
          mysiglist,msgbox = self.mycantrx.initrxsig(self.dictACFlg)
          for i in range(30):
              mysigdict = self.mycantrx.mymsgrecv(mysiglist)
              time.sleep(0.1)

          if int(mysigdict['CCM_FLTempSts']) == 16 and int(mysigdict['CCM_FRTempSts']) == 22:
              self.mylogger.info('test7 pass')
         
          else:
              self.mylogger.info('test7 Fail')
              self.tsresult = False

          self.dictACFlg['flgacon'] = TsOFF
          mylistmsg,msgbox= self.mycantrx.inittxsig(self.dictACFlg,self.dictSigVal)
          for i in range(5):
              self.mycantrx.mymsgtx(mylistmsg)
              time.sleep(0.004)
          self.mylogger.info('-----------test7 over----------')

      def test8(self):
             #test8
          self.mylogger.info('------------test8 SYNONOFF test---------------')
          self.mylogger.info('test8')
          self.dictACFlg['flgacon'] = TsON
          mylistmsg,msgbox= self.mycantrx.inittxsig(self.dictACFlg,self.dictSigVal)
          for i in range(5):
              self.mycantrx.mymsgtx(mylistmsg)
              time.sleep(0.004)
          time.sleep(5)

          self.dictACFlg['flgacdual'] = TsSYNON
          mylistmsg,msgbox= self.mycantrx.inittxsig(self.dictACFlg,self.dictSigVal)
          for i in range(5):
              self.mycantrx.mymsgtx(mylistmsg)
              time.sleep(0.004)          

          time.sleep(1)
          mysiglist,msgbox = self.mycantrx.initrxsig(self.dictACFlg)
          for i in range(30):
              mysigdict = self.mycantrx.mymsgrecv(mysiglist)
              time.sleep(0.1)

          if mysigdict['CCM_SYNCSts'] == 0:
              self.mylogger.info('test8 Pass:CCM_SYNCSts=0')
          elif mysigdict['CCM_SYNCSts'] == 1:
             self.mylogger.info('test8 Fail:CCM_SYNCSts=1')
             self.tsresult = False
          else:
              self.mylogger.info('test8 Fail:CCM_SYNCSts=None')
              self.tsresult = False

          self.dictACFlg['flgacdual'] = TsSYNOFF
          mylistmsg,msgbox= self.mycantrx.inittxsig(self.dictACFlg,self.dictSigVal)
          for i in range(5):
              self.mycantrx.mymsgtx(mylistmsg)
              time.sleep(0.004)

          time.sleep(5)
          mysiglist,msgbox = self.mycantrx.initrxsig(self.dictACFlg)
          for i in range(30):
              mysigdict = self.mycantrx.mymsgrecv(mysiglist)
              time.sleep(0.1)

          if mysigdict['CCM_SYNCSts'] == 1:
              self.mylogger.info('test8 Pass:CCM_SYNCSts=1')
          elif mysigdict['CCM_SYNCSts'] == 0:
             self.mylogger.info('test8 Fail:CCM_SYNCSts=0')
             self.tsresult = False
          else:
              self.mylogger.info('test8 Fail:CCM_SYNCSts=None')
              self.tsresult = False

          self.dictACFlg['flgacon'] = TsOFF
          mylistmsg,msgbox= self.mycantrx.inittxsig(self.dictACFlg,self.dictSigVal)
          for i in range(5):
              self.mycantrx.mymsgtx(mylistmsg)
              time.sleep(0.004)
          time.sleep(5)
          self.mylogger.info('-----------test8 over----------')  