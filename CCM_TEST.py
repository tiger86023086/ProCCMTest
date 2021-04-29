# -*- coding: utf-8 -*-

#  CCM TEST.py
#
#  ~~~~~~~~~~~~
#
#  Function GUI MainWindow Thread
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

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
#from future_builtins import *


from PyQt5.QtCore import (Qt,QTimer,QReadWriteLock,QDir)
from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtCore import pyqtSlot as Slot
from PyQt5.QtWidgets import (QApplication, QMainWindow,QDialog,QFileDialog,QWidget,QAction)
import ui_MainWindow,ui_HMIAC,ui_Matrix

import os,sys

import acthread
import dbthread




class MainWin(QMainWindow,
           ui_MainWindow.Ui_MainWindow):

      def __init__(self,parent=None):
            super(MainWin,self).__init__(parent)

            self.__diaexec = False
            self.canbox = ''
            self.DBCdir = ''
##            self.__startflg = False
##            self.__stopflg = False
##
            self.listmessagebox=[]
            self.error=False
##            self.progressvalue=[]

            self.timer=QTimer(self)
            self.timer.timeout.connect(self.showtime)            

            #self.comboBoxSelectCANbox.currentIndexChanged.connect(self.selectionchange)            

##            self.thread.finished.connect(self.finished)
##            #self.thread1.result.connect(self.hsresult)
##
##            self.thread.stoped.connect(self.stoped)
                      
            self.setupUi(self)

      @Slot()
      def on_AirCondition_triggered(self):
            #print('aa')
            self.acdlg=AirCondition(parent=self)
            self.acdlg.show()

            #if self.acdlg.exec_():
            self.acdlg.canbox = self.canbox
            self.acdlg.dbfile = self.DBCdir

            

      @Slot()            
      def on_DBCreate_triggered(self):
            #print('bb')
            self.createdb=Matrix(parent=self)
            self.createdb.show()
      	    
      	    
      @Slot()
      def on_pushButtonDBC_clicked(self):
            
            DBCdir=QFileDialog.getExistingDirectory(self,"Select DBC",QString(os.getcwd()),QFileDialog.DontResolveSymlinks)
            self.DBCdir=QDir.convertSeparators(DBCdir)
            #print type(self.DBCdir)
            self.lineEditDBC.setText(self.DBCdir)
                  
      @Slot()
      def on_pushButtonOK_clicked(self):

            self.pushButtonOK.setEnabled(False)
            self.pushButtonOK.setStyleSheet("QPushButton{background-color: rgb(255, 0, 0);"\
                                            "border-radius: 30px;  border: 2px groove gray;}")            
            if self.__diaexec:
                  #self.textBrowser.append("aaa")

                  self.canbox = self.comboBox_selectCANbox.currentText()
                                    
                  self.timer.start(1)
##                  self.thread.initialize(self.casedir,self.usermapdir,self.a2ldir,self.HILName,self.modelmapdir,\
##                  self.listmessagebox,self.progressvalue,self.error)
##                  self.thread.start()

##                  self.diaprogress = progress(parent=None)
##                  self.diaprogress.show()
                  
                  
            #self.textBrowser.append("aaa")
      
##      def selectionchange(self):
##            
##            self.canbox = self.comboBoxSelectCANbox.currentText()
##            self.pushButtonOK.setEnabled(True)
            
      @Slot()
      def on_pushButtonClear_clicked(self):
            self.textBrowser.clear()
            self.lineEditDBC.setText("")
            self.pushButtonOK.setEnabled(True)
            self.pushButtonOK.setStyleSheet("QPushButton{background-color: rgb(199, 237, 204);"\
                                            "border-radius: 30px;  border: 2px groove gray;}")

      def showtime(self):

            self.textBrowser.clear()

            for prt in self.listmessagebox:
                  self.textBrowser.append(prt)                  
            
class AirCondition(QDialog,
        ui_HMIAC.Ui_HMIDialog):
      def __init__(self,parent=None):
            super(AirCondition,self).__init__(parent)

            self.dictACFlg={'flgacon':0,
                            'flgacauto':0,
                            'flgacac':0,
                            'flgacrec':0,
                            'valacbl':0,
                            'flgacdef':0,
                            'flgacwindow':0,
                            'flgacface':0,
                            'flgacfoot':0,
                            'valacltemp':0,
                            'valacrtemp':0,
                            'flgacdual':0,
                            'flgacldef':0,
                            'flgaclauto':0}
            
            self.dictSigVal={'vspd':0,
                             'battcooltemp':0,
                             'battheattemp':0,
                             'ptcpwr':0,
                             'comppwr':0}
##
            self.flgacrun = 0
##            #self.flgsigrun = 0
##            
            self.listmessageboxfile=[]
            self.listmessageboxinsert=[]
##
            self.canbox = ''
            self.dbfile = ''
##
##            self.timer=QTimer(self)
##            self.timer.timeout.connect(self.showtime)
##            
            self.thread=acthread.ACThread()
##            #self.thread.result.connect(self.hsresult)

            self.setModal(True)#True为模态对话框，False为非模态对话框
            
            self.setupUi(self)

      @Slot()
      def on_pushButtonACStart_clicked(self):
            if not self.flgacrun:
                  self.pushButtonACStart.setStyleSheet("QPushButton{background-color: rgb(255, 0, 0);border-radius: 30px;  border: 2px groove gray;}")
                  self.pushButtonACStop.setStyleSheet("QPushButton{background-color: rgb(199, 237, 204);border-radius: 30px;  border: 2px groove gray;}")
                  self.flgacrun = 1

##                  self.thread.initialize(self.canbox,
##                                         self.dbfile,
##                                         self.flgacrun,
##                                         self.flgsigrun,
##                                         self.dictACFlg,
##                                         self.dictSigVal)
##                  self.thread.start()
                  
            else:
                  pass

            #print(self.flgacrun)

      @Slot()
      def on_pushButtonACStop_clicked(self):
            if self.flgacrun:
                  self.pushButtonACStop.setStyleSheet("QPushButton{background-color: rgb(255, 0, 0);border-radius: 30px;  border: 2px groove gray;}")
                  #self.pushButtonACStart.("QPushButton:pressed{background-color: rgb(199, 237, 204);}")
                  self.pushButtonACStart.setStyleSheet("QPushButton{background-color: rgb(199, 237, 204);border-radius: 30px;  border: 2px groove gray;}")
                  self.flgacrun = 0
##                  self.thread.wait()
            else:
                  pass
            
      @Slot()
      def on_pushButtonON_clicked(self):

            if self.flgacrun:
                  if self.dictACFlg['flgacon'] == 0:
                        self.dictACFlg['flgacon'] = 1
                  elif self.dictACFlg['flgacon'] == 1:
                        self.dictACFlg['flgacon'] = 0
                  else:
                        print('Error Value!')
            else:
                  pass
            #self.pushButtonON.setStyleSheet("QPushButton:pressed{background-color: rgb(255, 0, 0)}")           

      @Slot()
      def on_pushButtonAUTO_clicked(self):

            if self.flgacrun:
                  if self.dictACFlg['flgacauto'] == 0:
                        self.dictACFlg['flgacauto'] = 1
                  elif self.dictACFlg['flgacauto'] == 1:
                        self.dictACFlg['flgacauto'] = 0
                  else:
                        print('Error Value!')
            else:
                  pass            
     
      @Slot()
      def on_pushButtonAC_clicked(self):

            if self.flgacrun:
                  if self.dictACFlg['flgacac'] == 0:
                        self.dictACFlg['flgacac'] = 1
                  elif self.dictACFlg['flgacac'] == 1:
                        self.dictACFlg['flgacac'] = 0
                  else:
                        print('Error Value!')
            else:
                  pass            
            
      @Slot()            
      def on_pushButtonREC_clicked(self):

            if self.flgacrun:
                  if self.dictACFlg['flgacrec'] == 0:
                        self.dictACFlg['flgacrec'] = 1
                  elif self.dictACFlg['flgacrec'] == 1:
                        self.dictACFlg['flgacrec'] = 0
                  else:
                        print('Error Value!')
            else:
                  pass

      @Slot()            
      def on_pushButtonBLSub_clicked(self):

            if self.flgacrun:
                  blvalue = eval(self.lineEditBLVal.text())
                  if blvalue == 1:
                        pass
                  else:
                       blvalue = blvalue-1 
                       self.dictACFlg['valacbl'] = blvalue
                       self.lineEditBLVal.setText(str(blvalue))

            else:
                  pass

      @Slot()            
      def on_pushButtonBLPlus_clicked(self):

##            print(self.flgacrun)
##            print(self.lineEditBLVal.text())
            #self.lineEditBLVal.setText('7')
##            #print(type(self.lineEditBLVal.Text()))
            if self.flgacrun:
                  
                  blvalue = eval(self.lineEditBLVal.text())
##                  print(blvalue)
                  if blvalue == 7:
                        pass
                  else:
                       blvalue = blvalue+1 
                       self.dictACFlg['valacbl'] = blvalue
                       self.lineEditBLVal.setText(str(blvalue))

            else:
                  pass

      @Slot()
      def on_pushButtonLTempSub_clicked(self):

            if self.flgacrun:
                    ltempvalue = eval(self.lineEditTempL.text())
                    if ltempvalue == 16:
                          pass
                    else:
                         ltempvalue = ltempvalue-0.5 
                         self.dictACFlg['valacltemp'] = ltempvalue
                         self.lineEditTempL.setText(str(ltempvalue))                 

            else:
                    pass

      @Slot()
      def on_pushButtonLTempPlus_clicked(self):

            if self.flgacrun:
                    ltempvalue = eval(self.lineEditTempL.text())
                    if ltempvalue == 32:
                          pass
                    else:
                         ltempvalue = ltempvalue+0.5 
                         self.dictACFlg['valacltemp'] = ltempvalue
                         self.lineEditTempL.setText(str(ltempvalue))

            else:
                  pass

      @Slot()
      def on_pushButtonRTempSub_clicked(self):

            if self.flgacrun:
                    rtempvalue = eval(self.lineEditTempR.text())
                    if rtempvalue == 16:
                          pass
                    else:
                         rtempvalue = rtempvalue-0.5 
                         self.dictACFlg['valacrtemp'] = rtempvalue
                         self.lineEditTempR.setText(str(rtempvalue))

            else:
                  pass

      @Slot()
      def on_pushButtonRTempPlus_clicked(self):

            if self.flgacrun:
                    rtempvalue = eval(self.lineEditTempR.text())
                    if rtempvalue == 32:
                          pass
                    else:
                         rtempvalue = rtempvalue+0.5 
                         self.dictACFlg['valacltemp'] = rtempvalue
                         self.lineEditTempR.setText(str(rtempvalue))

            else:
                  pass    
            
      @Slot()            
      def on_pushButtonDEF_clicked(self):

            if self.flgacrun:
                  if self.dictACFlg['flgacdef'] == 0:
                        self.dictACFlg['flgacdef'] = 1
                  elif self.dictACFlg['flgacdef'] == 1:
                        self.dictACFlg['flgacdef'] = 0
                  else:
                        print('Error Value!')
            else:
                  pass            
            
      @Slot()            
      def on_pushButtonWindow_clicked(self):

            if self.flgacrun:
                  if self.dictACFlg['flgacwindow'] == 0:
                        self.dictACFlg['flgacwindow'] = 1
                  elif self.dictACFlg['flgacwindow'] == 1:
                        self.dictACFlg['flgacwindow'] = 0
                  else:
                        print('Error Value!')
            else:
                  pass            
                
      @Slot()            
      def on_pushButtonFace_clicked(self):

            if self.flgacrun:
                  if self.dictACFlg['flgacface'] == 0:
                        self.dictACFlg['flgacface'] = 1
                  elif self.dictACFlg['flgacface'] == 1:
                        self.dictACFlg['flgacface'] = 0
                  else:
                        print('Error Value!')
            else:
                  pass
            
      @Slot()            
      def on_pushButtonFoot_clicked(self):

           if self.flgacrun:
                  if self.dictACFlg['flgacfoot'] == 0:
                        self.dictACFlg['flgacfoot'] = 1
                  elif self.dictACFlg['flgacfoot'] == 1:
                        self.dictACFlg['flgacfoot'] = 0
                  else:
                        print('Error Value!')
           else:
                  pass 

      @Slot()            
      def on_pushButtonLDef_clicked(self):

           if self.flgacrun:
                  if self.dictACFlg['flgacldef'] == 0:
                        self.dictACFlg['flgacldef'] = 1
                  elif self.dictACFlg['flgacldef'] == 1:
                        self.dictACFlg['flgacldef'] = 0
                  else:
                        print('Error Value!')
           else:
                  pass

      @Slot()            
      def on_pushButtonLAuto_clicked(self):

            if self.flgacrun:
                  if self.dictACFlg['flgaclauto'] == 0:
                        self.dictACFlg['flgaclauto'] = 1
                  elif self.dictACFlg['flgaclauto'] == 1:
                        self.dictACFlg['flgaclauto'] = 0
                  else:
                        print('Error Value!')
            else:
                  pass

      @Slot()            
      def on_radioButtonDual_clicked(self):

            if self.flgacrun:
                  if self.radioButtonDual.isChecked():
                        self.dictACFlg['flgacdual'] = 1

                  else:
                        self.dictACFlg['flgacdual'] = 0
                  
            else:
                  pass

    

    
##
##      @Slot()
##      def on_pushButtonSigStart_clicked(self):
##            if not self.flgsigrun:
##                  self.pushButtonSigStart.setStyleSheet("QPushButton{background-color: rgb(255, 0, 0)"\
##                                                        "border-radius: 30px;  border: 2px groove gray;}")
##                  self.flgsigrun = 1
##            else:
##                  pass
##
##      @Slot()
##      def on_pushButtonSigStop_clicked(self):
##            if self.flgsigrun:
##                  self.pushButtonSigStop.setStyleSheet("QPushButton{background-color: rgb(255, 0, 0)"\
##                                                       "border-radius: 30px;  border: 2px groove gray;}")
##                  #self.pushButtonACStart.("QPushButton:pressed{background-color: rgb(199, 237, 204);}")
##                  self.pushButtonSigStart.setStyleSheet("QPushButton{background-color: rgb(199, 237, 204)"\
##                                                        "border-radius: 30px;  border: 2px groove gray;}")
##                  self.flgsigrun = 0
##            else:
##                  pass

##      def showtime(self):
##            pass
##
##      def hsresult(self):
##            self.thread.wait()
##            self.timer.stop()
            
            

class Matrix(QDialog,
        ui_Matrix.Ui_MatrixDlg):
      def __init__(self,parent=None):
            super(Matrix,self).__init__(parent)
            
            self.DBCdir=''
            self.setModal(True)#True为模态对话框，False为非模态对话框

            self.listmessageboxfile=[]
            self.listmessageboxinsert=[]

            self.timer1=QTimer(self)
            self.timer1.timeout.connect(self.showtime1)

            self.thread1 = dbthread.DBThread()
            self.thread1.result.connect(self.hsresult)
            
            
            self.setupUi(self)
      @Slot()
      def on_pushButtonDBC_clicked(self):
            
            DBCdir=QFileDialog.getExistingDirectory(self,"Select DBC",QString(os.getcwd()),QFileDialog.DontResolveSymlinks)
            self.DBCdir=QDir.convertSeparators(DBCdir)
            #print type(self.DBCdir)
            self.lineEditDBC.setText(self.DBCdir)

      @Slot()
      def on_pushButtonGen_clicked(self):
            self.pushButtonGen.setEnabled(False)
            self.thread1.initialize(self.DBCdir,self.listmessageboxfile,self.listmessageboxinsert)
            self.timer1.start(1)
            self.thread1.start()            

      def hsresult(self):
            self.thread1.wait()
            self.timer1.stop()
            self.pushButtonGen.setEnabled(True)           	
            
      def showtime1(self):

            self.textBrowserfile.clear()
            self.textBrowserinsert.clear()
            
            if len(self.listmessageboxfile):
                  for prt in self.listmessageboxfile:
                        self.textBrowserfile.append(prt)

            if len(self.listmessageboxinsert):

                  for prt in self.listmessageboxinsert:
                        self.textBrowserinsert.append(prt)  
            
##            self.textBrowserfile.append(self.listmessageboxfile[0])
##            self.textBrowserinsert.append(self.listmessageboxinsert[0])     
            



if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    form=MainWin()
    form.show()
    sys.exit(app.exec_())
