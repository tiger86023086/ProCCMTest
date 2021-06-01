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
#  Last change: 01.06.2021 Li Yonghu 
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

import acthread
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
            self.canbox = ''
            self.dbfile = ''
            self.mycantrx = None

            self.dictACFlg={'flgacon':0,
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
            
            self.dictSigVal={'vspd':0,
                             'battcooltemp':0,
                             'battheattemp':0,
                             'ptcpwr':0,
                             'comppwr':0}
##
            self.flgacrun = 0
            self.flgbutton = 0
##            self.thread=acthread.ACThread()

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
##                  self.getdata1()
##                  self.getdata2()
                  canbox = self.comboBoxSelectCANbox.currentText()
                  dbfile = self.DBCdirfile
                  self.mycantrx = myctrlcan(dbfile,canbox)
                  mylistmsg = self.mycantrx.inittxsig(self.dictACFlg,self.dictSigVal)
                  self.mycantrx.mymsgtxperiod(mylistmsg)

                  self.timer.start(1)
##                  print(self.canbox)
##                  print(self.dbfile)
##                  print(self.flgacrun)
##                  print(self.mycantrx)
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
                        self.mycantrx.stopsendperiod()
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
                  
                  if self.dictACFlg['flgacon'] == 0:
                        self.dictACFlg['flgacon'] = 1
                        self.pushButtonON.setStyleSheet("QPushButton{background-color: rgb(255, 0, 0);border-radius: 20px;  border: 2px groove gray;font: 12pt 'Arial'}")
                        self.flgbutton = 1
                  elif self.dictACFlg['flgacon'] == 1:
                        self.dictACFlg['flgacon'] = 0
                        self.pushButtonON.setStyleSheet("QPushButton{border-radius: 20px;  border: 2px groove gray;font: 12pt 'Arial'}")
                        self.flgbutton = 1
                  else:
                        print('Error Value!')
            else:
                  pass
            #self.pushButtonON.setStyleSheet("QPushButton:pressed{background-color: rgb(255, 0, 0)}")           

      @Slot()
      def on_pushButtonAUTO_clicked(self):

            if self.flgacrun:
                  if self.dictACFlg['flgacauto'] == 0:
                        self.dictACFlg['flgacauto'] = 12
                        self.pushButtonAUTO.setStyleSheet("QPushButton{background-color: rgb(255, 0, 0);border-radius: 20px;  border: 2px groove gray;font: 12pt 'Arial'}")
                        self.flgbutton = 1
                  elif self.dictACFlg['flgacauto'] == 1:
                        self.dictACFlg['flgacauto'] = 0
                        self.pushButtonAUTO.setStyleSheet("QPushButton{border-radius: 20px;  border: 2px groove gray;font: 12pt 'Arial'}")
                        self.flgbutton = 1
                  else:
                        print('Error Value!')
            else:
                  pass            
     
      @Slot()
      def on_pushButtonAC_clicked(self):

            if self.flgacrun:
                  if self.dictACFlg['flgacac'] == 0:
                        self.dictACFlg['flgacac'] = 1
                        self.pushButtonAC.setStyleSheet("QPushButton{background-color: rgb(255, 0, 0);border-radius: 20px;  border: 2px groove gray;font: 12pt 'Arial'}")
                        self.flgbutton = 1
                  elif self.dictACFlg['flgacac'] == 1:
                        self.dictACFlg['flgacac'] = 0
                        self.pushButtonAC.setStyleSheet("QPushButton{border-radius: 20px;  border: 2px groove gray;font: 12pt 'Arial'}")
                        self.flgbutton = 1
                  else:
                        print('Error Value!')
            else:
                  pass            
            
      @Slot()            
      def on_pushButtonREC_clicked(self):

            if self.flgacrun:
                  if self.dictACFlg['flgacrec'] == 0:
                        self.dictACFlg['flgacrec'] = 1
                        self.pushButtonREC.setStyleSheet("QPushButton{background-color: rgb(255, 0, 0);border-radius: 20px;  border: 2px groove gray;font: 12pt 'Arial'}")
                        self.flgbutton = 1
                  elif self.dictACFlg['flgacrec'] == 1:
                        self.dictACFlg['flgacrec'] = 0
                        self.pushButtonREC.setStyleSheet("QPushButton{border-radius: 20px;  border: 2px groove gray;font: 12pt 'Arial'}")
                        self.flgbutton = 1
                  else:
                        print('Error Value!')
            else:
                  pass

      @Slot(int)
      def on_horizontalSliderBlwrLvl_valueChanged(self,value):
            if self.flgacrun:
                  self.dictACFlg['valacbl'] = value
                  self.displayBlwrLvl.display(value)
            else:
                  self.dictACFlg['valacbl'] = 1
                  self.displayBlwrLvl.display(1)

      @Slot(int)
      def on_scrollBarLeftTemp_valueChanged(self,value):
            if self.flgacrun:
                  self.lineEditTempL.setText(str(value))
                  
      @Slot(int)
      def on_scrollBarRightTemp_valueChanged(self,value):
            if self.flgacrun:
                  self.lineEditTempR.setText(str(value))     
            
      @Slot()            
      def on_pushButtonDEF_clicked(self):

            if self.flgacrun:
                  if self.dictACFlg['flgacdef'] == 0:
                        self.dictACFlg['flgacdef'] = 1
                        self.pushButtonDEF.setStyleSheet("QPushButton{background-color: rgb(255, 0, 0);border-radius: 20px;  border: 2px groove gray;font: 12pt 'Arial'}")
                        self.flgbutton = 1
                  elif self.dictACFlg['flgacdef'] == 1:
                        self.dictACFlg['flgacdef'] = 0
                        self.pushButtonDEF.setStyleSheet("QPushButton{border-radius: 20px;  border: 2px groove gray;font: 12pt 'Arial'}")
                        self.flgbutton = 1
                  else:
                        print('Error Value!')
            else:
                  pass            
            
      @Slot()            
      def on_pushButtonWindow_clicked(self):

            if self.flgacrun:
                  if self.dictACFlg['flgacwindow'] == 0:
                        self.dictACFlg['flgacwindow'] = 1
                        self.pushButtonWindow.setStyleSheet("QPushButton{background-color: rgb(255, 0, 0);border-radius: 20px;  border: 2px groove gray;font: 12pt 'Arial'}")
                        self.flgbutton = 1
                  elif self.dictACFlg['flgacwindow'] == 1:
                        self.dictACFlg['flgacwindow'] = 0
                        self.pushButtonWindow.setStyleSheet("QPushButton{border-radius: 20px;  border: 2px groove gray;font: 12pt 'Arial'}")
                        self.flgbutton = 1
                  else:
                        print('Error Value!')
            else:
                  pass            
                
      @Slot()            
      def on_pushButtonFace_clicked(self):

            if self.flgacrun:
                  if self.dictACFlg['flgacface'] == 0:
                        self.dictACFlg['flgacface'] = 1
                        self.pushButtonFace.setStyleSheet("QPushButton{background-color: rgb(255, 0, 0);border-radius: 20px;  border: 2px groove gray;font: 12pt 'Arial'}")
                        self.flgbutton = 1
                  elif self.dictACFlg['flgacface'] == 1:
                        self.dictACFlg['flgacface'] = 0
                        self.pushButtonFace.setStyleSheet("QPushButton{border-radius: 20px;  border: 2px groove gray;font: 12pt 'Arial'}")
                        self.flgbutton = 1
                  else:
                        print('Error Value!')
            else:
                  pass
            
      @Slot()            
      def on_pushButtonFoot_clicked(self):

           if self.flgacrun:
                  if self.dictACFlg['flgacfoot'] == 0:
                        self.dictACFlg['flgacfoot'] = 1
                        self.pushButtonFoot.setStyleSheet("QPushButton{background-color: rgb(255, 0, 0);border-radius: 20px;  border: 2px groove gray;font: 12pt 'Arial'}")
                        self.flgbutton = 1
                  elif self.dictACFlg['flgacfoot'] == 1:
                        self.dictACFlg['flgacfoot'] = 0
                        self.pushButtonFoot.setStyleSheet("QPushButton{border-radius: 20px;  border: 2px groove gray;font: 12pt 'Arial'}")
                        self.flgbutton = 1
                  else:
                        print('Error Value!')
           else:
                  pass 

##      @Slot()            
##      def on_pushButtonLDef_clicked(self):
##
##           if self.flgacrun:
##                  if self.dictACFlg['flgacldef'] == 0:
##                        self.dictACFlg['flgacldef'] = 1
##                  elif self.dictACFlg['flgacldef'] == 1:
##                        self.dictACFlg['flgacldef'] = 0
##                  else:
##                        print('Error Value!')
##           else:
##                  pass
##
##      @Slot()            
##      def on_pushButtonLAuto_clicked(self):
##
##            if self.flgacrun:
##                  if self.dictACFlg['flgaclauto'] == 0:
##                        self.dictACFlg['flgaclauto'] = 1
##                  elif self.dictACFlg['flgaclauto'] == 1:
##                        self.dictACFlg['flgaclauto'] = 0
##                  else:
##                        print('Error Value!')
##            else:
##                  pass

      @Slot()            
      def on_radioButtonDual_clicked(self):            

            if self.flgacrun:
                  if self.radioButtonDual.isChecked():
                        self.dictACFlg['flgacdual'] = 1
                        self.flgbutton = 1

                  else:
                        self.dictACFlg['flgacdual'] = 0
                        self.flgbutton = 1
                  
            else:
                  pass

##      def getdata(self,mycantrx):
##            self.mycantrx = mycantrx
####            self.dbfile = dbfile
####            print(self.dbfile)
####            print(self.canbox)
##      
##      def hsresult(self):
##            self.thread.wait()

      def showtime(self):

            if self.flgbutton:                                    
                  mylistmsg = self.mycantrx.inittxsig(self.dictACFlg,self.dictSigVal)
                  mysiglist = self.mycantrx.initrxsig(self.dictACFlg)
                  #print('aaaaa')
                  for i in range(5):
                        #print('bbbbb') 
                        self.mycantrx.mymsgtx(mylistmsg)
                        time.sleep(0.004)
                  self.flgbutton = 0
                                   
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
