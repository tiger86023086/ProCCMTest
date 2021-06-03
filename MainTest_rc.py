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
#  Build: 19.05.2021
#  Last change: 02.06.2021 Li Yonghu 
#
#  Language: Python 3.7  PyQt5.15.2
#  ------------------------------------------------------------------
#  GNU GPL
#  
 
#

# Module Imports

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
#from future_builtins import *


from PyQt5.QtCore import (Qt,QTimer,QReadWriteLock,QDir)
from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtCore import pyqtSlot as Slot
from PyQt5.QtWidgets import (QApplication, QMainWindow,QDialog,QFileDialog,QWidget,QAction)
import ui_MainWindow,ui_HMIAC,ui_Matrix

import qdarkstyle  # noqa: E402
from qdarkstyle.dark.palette import DarkPalette  # noqa: E402
from qdarkstyle.light.palette import LightPalette  # noqa: E402

import os,sys
import time

import cantxthread
import canrxthread
import dbthread

import ctrlcantrx
from myctrlcan import myctrlcan

class MainWin(QMainWindow,
           ui_MainWindow.Ui_MainWindow):

      canbox  = Signal(str)
      dbfile = Signal(str)

      def __init__(self,parent=None):
            super(MainWin,self).__init__(parent)

##            self.__diaexec = False
            self.listmessagebox=[]
            self.error=False
##            self.progressvalue=[]
##            self.canbox = ''
##            self.dbfile = ''
            self.mycantrx = None

            self.flagacon = False
            self.flgacauto = False
            self.flgacac = False
            self.flgacrec = False
            self.flgacdef = False
            self.flgacwindow = False
            self.flgacface = False
            self.flgacfoot = False

            self.initacsig()
            self.initsigval()           
            
            
##
            self.flgacrun = 0
            self.flgbutton = 0
            self.mysigdict = dict()
            self.txthread=cantxthread.TxThread()
            self.rxthread = canrxthread.RxThread()
            self.rxthread.redict.connect(self.getdata)

            self.timer=QTimer(self)
            self.timer.timeout.connect(self.showtime)            

                      
            self.setupUi(self)

      @Slot()
      def on_actionDarkStyle_triggered(self):
            #print('aa')
            style = qdarkstyle.load_stylesheet(palette=DarkPalette)
            self.setStyleSheet(style)
                       

      @Slot()            
      def on_actionLightStyle_triggered(self):
            #print('bb')
            style = qdarkstyle.load_stylesheet(palette=LightPalette)
            self.setStyleSheet(style)
            
      	    
      @Slot()
      def on_pushButtonDBC_clicked(self):
            
            self.DBCdirfile,filetype=QFileDialog.getOpenFileName(self,
                                                    "Select DBC File",
                                                    os.getcwd(),
                                                    "DBC Files (*.dbc);;LDF Files (*.ldf)")
            #self.DBCdir=QDir.convertSeparators(DBCdir)
            #print type(self.DBCdir)
            self.lineEditDBC.setText(self.DBCdirfile)
                  

      @Slot()
      def on_pushButtonACStart_clicked(self):
            if not self.flgacrun:
                  self.pushButtonACStart.setStyleSheet("QPushButton{background-color: rgb(255, 0, 0);border-radius: 20px;  border: 2px groove gray;font: 12pt 'Arial'}")
                  self.pushButtonACStop.setStyleSheet("QPushButton{border-radius: 20px;  border: 2px groove gray;font: 12pt 'Arial'}")           
                  
                  self.flgacrun = 1
                  self.mycantrx = None
                  
                  canbox = self.comboBoxSelectCANbox.currentText()
                  dbfile = self.DBCdirfile
                  self.mycantrx = myctrlcan(dbfile,canbox)                  
                  mylistmsg = self.mycantrx.inittxsig(self.dictACFlg,self.dictSigVal)                  
                  self.mycantrx.mymsgtxperiod(mylistmsg)

                  self.timer.start(1)
            else:
                  pass

            #print(self.flgacrun)

      @Slot()
      def on_pushButtonACStop_clicked(self):
            if self.flgacrun:
                  self.pushButtonACStop.setStyleSheet("QPushButton{background-color: rgb(255, 0, 0);border-radius: 20px;  border: 2px groove gray;font: 12pt 'Arial'}")
                  #self.pushButtonACStart.setStyleSheet("QPushButton:pressed{background-color: rgb(199, 237, 204);border-radius: 20px;}")
                  self.pushButtonACStart.setStyleSheet("QPushButton{border-radius: 20px;  border: 2px groove gray;font: 12pt 'Arial'}")
                  if self.flgacrun == 1:
                        self.mycantrx.mymsgstop()
                        self.timer.stop()
                  self.flgacrun = 0                  
                  if self.mycantrx != None:
##                        print('dbbbb')
                        self.mycantrx.mydelcan()
                        self.mycantrx = None                 
            else:
                  pass
            
      @Slot()
      def on_pushButtonON_clicked(self):

            if self.flgacrun:
                  self.initacsig()
                  
                  if not self.flagacon:
                        self.dictACFlg['flgacon'] = 1
                        self.pushButtonON.setStyleSheet("QPushButton{background-color: rgb(255, 0, 0);border-radius: 20px;  border: 2px groove gray;font: 12pt 'Arial'}")
                        self.flgbutton = 1
                        
                        
                  elif self.flagacon:
                        self.dictACFlg['flgacon'] = 0
                        self.pushButtonON.setStyleSheet("QPushButton{border-radius: 20px;  border: 2px groove gray;font: 12pt 'Arial'}")
                        self.flgbutton = 1                        
                        
                  else:
                        print('Error Value!')

                  if self.dictACFlg['flgacon'] == 1:
                        self.flagacon = True
                  elif self.dictACFlg['flgacon'] == 0:
                        self.flagacon = False
                  else:
                        self.flagacon = False
                        
            else:
                  pass
            #self.pushButtonON.setStyleSheet("QPushButton:pressed{background-color: rgb(255, 0, 0)}")           

      @Slot()
      def on_pushButtonAUTO_clicked(self):

            if self.flgacrun:
                  self.initacsig()
                  if not self.flgacauto:
                        self.dictACFlg['flgacauto'] = 1
                        self.pushButtonAUTO.setStyleSheet("QPushButton{background-color: rgb(255, 0, 0);border-radius: 20px;  border: 2px groove gray;font: 12pt 'Arial'}")
                        self.flgbutton = 1
                        
                  elif self.flgacauto:
                        self.dictACFlg['flgacauto'] = 0
                        self.pushButtonAUTO.setStyleSheet("QPushButton{border-radius: 20px;  border: 2px groove gray;font: 12pt 'Arial'}")
                        self.flgbutton = 1
                        
                  else:
                        print('Error Value!')

                  if self.dictACFlg['flgacauto'] == 1:
                        self.flgacauto = True
                  elif self.dictACFlg['flgacauto'] == 0:
                        self.flgacauto = False
                  else:
                        self.flgacauto = False
            else:
                  pass            
     
      @Slot()
      def on_pushButtonAC_clicked(self):

            if self.flgacrun:
                  self.initacsig()
                  if not self.flgacac:
                        self.dictACFlg['flgacac'] = 1
                        self.pushButtonAC.setStyleSheet("QPushButton{background-color: rgb(255, 0, 0);border-radius: 20px;  border: 2px groove gray;font: 12pt 'Arial'}")
                        self.flgbutton = 1
                        
                  elif self.flgacac:
                        self.dictACFlg['flgacac'] = 0
                        self.pushButtonAC.setStyleSheet("QPushButton{border-radius: 20px;  border: 2px groove gray;font: 12pt 'Arial'}")
                        self.flgbutton = 1
                        
                  else:
                        print('Error Value!')

                  if self.dictACFlg['flgacac'] == 1:
                        self.flgacac = True
                  elif self.dictACFlg['flgacac'] == 0:
                        self.flgacac = False
                  else:
                        self.flgacac = False
            else:
                  pass            
            
      @Slot()            
      def on_pushButtonREC_clicked(self):

            if self.flgacrun:
                  self.initacsig()
                  if not self.flgacrec:
                        self.dictACFlg['flgacrec'] = 1
                        self.pushButtonREC.setStyleSheet("QPushButton{background-color: rgb(255, 0, 0);border-radius: 20px;  border: 2px groove gray;font: 12pt 'Arial'}")
                        self.flgbutton = 1
                        
                  elif self.flgacrec:
                        self.dictACFlg['flgacrec'] = 0
                        self.pushButtonREC.setStyleSheet("QPushButton{border-radius: 20px;  border: 2px groove gray;font: 12pt 'Arial'}")
                        self.flgbutton = 1
                        
                  else:
                        print('Error Value!')

                  if self.dictACFlg['flgacrec'] == 1:
                        self.flgacrec = True
                  elif self.dictACFlg['flgacrec'] == 0:
                        self.flgacrec = False
                  else:
                        self.flgacrec = False
            else:
                  pass

      @Slot(int)
      def on_horizontalSliderBlwrLvl_valueChanged(self,value):
            if self.flgacrun:
                  self.initacsig()
                  self.dictACFlg['valacbl'] = value-1
                  self.displayBlwrLvl.display(value)
                  self.flgbutton = 1
            else:
                  self.dictACFlg['valacbl'] = 1
                  self.displayBlwrLvl.display(1)

      @Slot(int)
      def on_scrollBarLeftTemp_valueChanged(self,value):
            if self.flgacrun:
                  self.initacsig()
                  self.lineEditTempL.setText(str(value))
                  self.dictACFlg['valacltemp'] = value
                  self.flgbutton = 1
                  
      @Slot(int)
      def on_scrollBarRightTemp_valueChanged(self,value):
            if self.flgacrun:
                  self.initacsig()
                  self.lineEditTempR.setText(str(value))
                  self.dictACFlg['valacrtemp'] = value
                  self.flgbutton = 1
            
      @Slot()            
      def on_pushButtonDEF_clicked(self):

            if self.flgacrun:
                  self.initacsig()
                  if not self.flgacdef:
                        self.dictACFlg['flgacdef'] = 1
                        self.pushButtonDEF.setStyleSheet("QPushButton{background-color: rgb(255, 0, 0);border-radius: 20px;  border: 2px groove gray;font: 12pt 'Arial'}")
                        self.flgbutton = 1
                        
                  elif self.flgacdef:
                        self.dictACFlg['flgacdef'] = 0
                        self.pushButtonDEF.setStyleSheet("QPushButton{border-radius: 20px;  border: 2px groove gray;font: 12pt 'Arial'}")
                        self.flgbutton = 1
                        
                  else:
                        print('Error Value!')
                  if self.dictACFlg['flgacdef'] == 1:
                        self.flgacdef = True
                  elif self.dictACFlg['flgacdef'] == 0:
                        self.flgacdef = False
                  else:
                        self.flgacdef = False
            else:
                  pass            
            
      @Slot()            
      def on_pushButtonWIN_clicked(self):

            if self.flgacrun:
                  self.initacsig()

                  if not self.flgacwindow:
                        self.pushButtonWIN.setStyleSheet("QPushButton{background-color: rgb(255, 0, 0);border-radius: 20px;  border: 2px groove gray;font: 12pt 'Arial'}")
                        self.flgbutton = 1
                        if  self.flgacfoot:
                              self.dictACFlg['flgacmode'] = 3
                        else:
                              self.dictACFlg['flgacmode'] = 4                       
                  elif self.flgacwindow:                        
                        self.flgbutton = 1
                        if  self.flgacfoot:
                              self.pushButtonWIN.setStyleSheet("QPushButton{border-radius: 20px;  border: 2px groove gray;font: 12pt 'Arial'}")
                              self.dictACFlg['flgacmode'] = 2
                        elif self.flgacface:
                              self.pushButtonWIN.setStyleSheet("QPushButton{border-radius: 20px;  border: 2px groove gray;font: 12pt 'Arial'}")
                              self.dictACFlg['flgacmode'] = 0
                        elif self.flgacfoot and self.flgacface:
                              self.pushButtonWIN.setStyleSheet("QPushButton{border-radius: 20px;  border: 2px groove gray;font: 12pt 'Arial'}")
                              self.dictACFlg['flgacmode'] = 1
                        else:
                              self.dictACFlg['flgacmode'] = 4                                                    
                  else:
                        print('Error Value!')

                  if self.dictACFlg['flgacmode'] == 4 or self.dictACFlg['flgacmode'] == 3:
                        self.flgacwindow = True                  
                  else:
                        self.flgacwindow = False
            else:
                  pass            
                
      @Slot()            
      def on_pushButtonFACE_clicked(self):

            if self.flgacrun:
                  self.initacsig()
                  if not self.flgacface:
                        self.pushButtonFACE.setStyleSheet("QPushButton{background-color: rgb(255, 0, 0);border-radius: 20px;  border: 2px groove gray;font: 12pt 'Arial'}")
                        self.flgbutton = 1
                        if  self.flgacfoot:
                              self.dictACFlg['flgacmode'] = 1
                        else:
                             self.dictACFlg['flgacmode'] = 0                        
                  elif self.flgacface:                        
                        self.flgbutton = 1
                        if self.flgacfoot:
                              self.pushButtonFACE.setStyleSheet("QPushButton{border-radius: 20px;  border: 2px groove gray;font: 12pt 'Arial'}")
                              self.dictACFlg['flgacmode'] = 2
                        elif self.flgacwindow:
                              self.pushButtonFACE.setStyleSheet("QPushButton{border-radius: 20px;  border: 2px groove gray;font: 12pt 'Arial'}")
                              self.dictACFlg['flgacmode'] = 4
                        elif self.flgacfoot and self.flgacwindow:
                              self.pushButtonFACE.setStyleSheet("QPushButton{border-radius: 20px;  border: 2px groove gray;font: 12pt 'Arial'}")
                              self.dictACFlg['flgacmode'] = 3
                        else:
                              self.dictACFlg['flgacmode'] = 0                       
                  else:
                        print('Error Value!')
                  
                  if self.dictACFlg['flgacmode'] == 1 or self.dictACFlg['flgacmode'] == 0:
                        self.flgacface = True                  
                  else:
                        self.flgacface = False
            else:
                  pass
            
      @Slot()            
      def on_pushButtonFOOT_clicked(self):
           if self.flgacrun:
                  self.initacsig()
                  if not self.flgacfoot:
                        self.pushButtonFOOT.setStyleSheet("QPushButton{background-color: rgb(255, 0, 0);border-radius: 20px;  border: 2px groove gray;font: 12pt 'Arial'}")
                        self.flgbutton = 1
                        if self.flgacwindow:
                              self.dictACFlg['flgacmode'] = 3
                        elif self.flgacface:
                              self.dictACFlg['flgacmode'] = 1
                        else:
                              self.dictACFlg['flgacmode'] = 2                       
                  elif self.flgacfoot:                        
                        self.flgbutton = 1
                        if self.flgacwindow:
                              self.pushButtonFOOT.setStyleSheet("QPushButton{border-radius: 20px;  border: 2px groove gray;font: 12pt 'Arial'}")
                              self.dictACFlg['flgacmode'] = 4
                        elif self.flgacface:
                              self.pushButtonFOOT.setStyleSheet("QPushButton{border-radius: 20px;  border: 2px groove gray;font: 12pt 'Arial'}")
                              self.dictACFlg['flgacmode'] = 0
                        else:
                              self.dictACFlg['flgacmode'] = 2                        
                  else:
                        print('Error Value!')

                  if self.dictACFlg['flgacmode'] == 1 or self.dictACFlg['flgacmode'] == 2 or self.dictACFlg['flgacmode'] == 3:
                        self.flgacfoot = True                  
                  else:
                        self.flgacfoot = False
           else:
                  pass
      @Slot()            
      def on_radioButtonDual_clicked(self):            

            if self.flgacrun:
                  self.initacsig()
                  if self.radioButtonDual.isChecked():
                        self.dictACFlg['flgacdual'] = 1
                        self.flgbutton = 1

                  else:
                        self.dictACFlg['flgacdual'] = 0
                        self.flgbutton = 1
                  
            else:
                  pass

      def getdata(self,mydict):
            self.mysigdict = mydict
            
      def showtime(self):            

            if self.flgbutton:
                  
                  self.txthread.init(self.mycantrx,self.dictACFlg,self.dictSigVal)                  
                  self.txthread.start()                  
                  self.flgbutton = 0
                  #self.txthread.wait()

            if self.flgacrun:
                  self.rxthread.init(self.mycantrx,self.dictACFlg)
                  self.rxthread.start()
##                 mysiglist = self.mycantrx.initrxsig(self.dictACFlg)
##                 mysigdict = self.mycantrx.mymsgrecv(mysiglist)
                  #print(self.mysigdict)
                  self.display(self.mysigdict)

      def display(self,mysigdict):
            if mysigdict != {}:
                  if mysigdict['CCM_Off'] == 1:
                        self.displayON.setStyleSheet("QPushButton{background-color: rgb(0, 255, 0)}")
                  elif mysigdict['CCM_Off'] == 0:
                        self.displayON.setStyleSheet("QPushButton{}")
                  else:
                        print('Cannot recieve signal--CCM_Off ')

                  if mysigdict['CCM_AUTOSts'] == 1:
                        self.displayAUTO.setStyleSheet("QPushButton{background-color: rgb(0, 255, 0)}")
                  elif mysigdict['CCM_AUTOSts'] == 0:
                        self.displayAUTO.setStyleSheet("QPushButton{}")
                  else:
                        print('Cannot recieve signal--CCM_AUTOSts ')

                  if mysigdict['CCM_ACSts'] == 1:
                        self.displayAC.setStyleSheet("QPushButton{background-color: rgb(0, 255, 0)}")
                  elif mysigdict['CCM_ACSts'] == 0:
                        self.displayAC.setStyleSheet("QPushButton{}")
                  else:
                        print('Cannot recieve signal--CCM_ACSts ')

                  if mysigdict['CCM_CycleStatus'] == 0:
                        self.dispalyREC.setStyleSheet("QPushButton{background-color: rgb(0, 255, 0)}")
                  elif mysigdict['CCM_CycleStatus'] == 1:
                        self.dispalyREC.setStyleSheet("QPushButton{}")
                  else:
                        print('Cannot recieve signal--CCM_CycleStatus ')

                  if mysigdict['CCM_FrontDefrostSts'] == 1:
                        self.displayDEF.setStyleSheet("QPushButton{background-color: rgb(0, 255, 0)}")
                  elif mysigdict['CCM_FrontDefrostSts'] == 0:
                        self.displayDEF.setStyleSheet("QPushButton{}")
                  else:
                        print('Cannot recieve signal--CCM_FrontDefrostSts ')

                  if mysigdict['CCM_ModelDisplay'] == 4:
                        self.displayWIN.setStyleSheet("QPushButton{background-color: rgb(0, 255, 0)}")
                        self.displayFOOT.setStyleSheet("QPushButton{}")
                        self.displayFACE.setStyleSheet("QPushButton{}")
                  elif mysigdict['CCM_ModelDisplay'] == 0:
                        self.displayFOOT.setStyleSheet("QPushButton{background-color: rgb(0, 255, 0)}")
                        self.displayWIN.setStyleSheet("QPushButton{}")
                        self.displayFACE.setStyleSheet("QPushButton{}")
                  elif mysigdict['CCM_ModelDisplay'] == 2:
                        self.displayFACE.setStyleSheet("QPushButton{background-color: rgb(0, 255, 0)}")
                        self.displayWIN.setStyleSheet("QPushButton{}")
                        self.displayFOOT.setStyleSheet("QPushButton{}")
                  elif mysigdict['CCM_ModelDisplay'] == 1:
                        self.displayFACE.setStyleSheet("QPushButton{background-color: rgb(0, 255, 0)}")
                        self.displayWIN.setStyleSheet("QPushButton{}")
                        self.displayFOOT.setStyleSheet("QPushButton{background-color: rgb(0, 255, 0)}")
                  elif mysigdict['CCM_ModelDisplay'] == 3:
                        self.displayWIN.setStyleSheet("QPushButton{background-color: rgb(0, 255, 0)}")
                        self.displayFACE.setStyleSheet("QPushButton{}")
                        self.displayFOOT.setStyleSheet("QPushButton{background-color: rgb(0, 255, 0)}")
                  else:
                        print('Cannot recieve signal--CCM_ModelDisplay ')
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
                            'flgacdual':3}
      def initsigval(self):
            self.dictSigVal={'vspd':0,
                             'battcooltemp':0,
                             'battheattemp':0,
                             'ptcpwr':0,
                             'comppwr':0}



                  
            
                                   
##            else:                  
##                  self.mycantrx.stopsendperiod()
##                  print('ccccc')

            

##            self.thread.initialize(self.canbox,
##                                         self.dbfile,
##                                         self.flgacrun,
##                                         self.dictACFlg,
##                                         self.dictSigVal)
##            self.thread.start()
##            self.thread.cantrx.connect(self.getdata)

            

##            self.textBrowser.clear()
##
##            for prt in self.listmessagebox:
##                  self.textBrowser.append(prt)                  
            

            

##class Matrix(QDialog,
##        ui_Matrix.Ui_MatrixDlg):
##      def __init__(self,parent=None):
##            super(Matrix,self).__init__(parent)
##            
##            self.DBCdir=''
##            self.setModal(True)#True为模态对话框，False为非模态对话框
##
##            self.listmessageboxfile=[]
##            self.listmessageboxinsert=[]
##
##            self.timer1=QTimer(self)
##            self.timer1.timeout.connect(self.showtime1)
##
##            self.thread1 = dbthread.DBThread()
##            self.thread1.result.connect(self.hsresult)
##            
##            
##            self.setupUi(self)
##      @Slot()
##      def on_pushButtonDBC_clicked(self):
##            
##            self.DBCdir=QFileDialog.getExistingDirectory(self,"Select DBC",os.getcwd(),QFileDialog.DontResolveSymlinks)
##            #self.DBCdir=QDir.convertSeparators(DBCdir)
##            #print type(self.DBCdir)
##            self.lineEditDBC.setText(self.DBCdir)
##
##      @Slot()
##      def on_pushButtonGen_clicked(self):
##            self.pushButtonGen.setEnabled(False)
##            self.thread1.initialize(self.DBCdir,
##                                    self.listmessageboxfile,
##                                    self.listmessageboxinsert)
##            self.timer1.start(1)
##            self.thread1.start()            
##
##      def hsresult(self):
##            self.thread1.wait()
##            self.timer1.stop()
##            self.pushButtonGen.setEnabled(True)           	
##            
##      def showtime1(self):
##
##            self.textBrowserfile.clear()
##            self.textBrowserinsert.clear()
##            
##            if len(self.listmessageboxfile):
##                  for prt in self.listmessageboxfile:
##                        self.textBrowserfile.append(prt)
##
##            if len(self.listmessageboxinsert):
##
##                  for prt in self.listmessageboxinsert:
##                        self.textBrowserinsert.append(prt)  
##            
####            self.textBrowserfile.append(self.listmessageboxfile[0])
####            self.textBrowserinsert.append(self.listmessageboxinsert[0])     
            



if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    form=MainWin()
    form.show()
    sys.exit(app.exec_())
