# -*- coding: utf-8 -*-

#  dbthread.py
#
#  ~~~~~~~~~~~~
#
#  Function GUI DB Thread
#
#  ~~~~~~~~~~~~
#
#  ------------------------------------------------------------------
#  Author : Li Yonghu
#  Build: 24.04.2021
#  Last change: 24.04.2021 Li Yonghu 
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
import traceback

from matrixrd import *

class DBThread(QThread):
      result = Signal(bool)
      def __init__(self,parent=None):
            super(DBThread,self).__init__(parent)
            
            self.dbcpath=None

      def initialize(self,dbcpath,listmessageboxfile,listmessageboxinsert):           
            self.dbcpath=dbcpath
            self.listmessageboxfile = listmessageboxfile
            self.listmessageboxinsert = listmessageboxinsert

      def run(self):         
            
            reflag=self.DBCreate(self.dbcpath)

            if reflag == True:
                  self.wait()
                  self.listmessageboxfile.append('All Database haved be created')
            else:
                  self.wait()
                  self.listmessageboxfile.append('It generate error when creating Database')

            self.result.emit(True)            

      def DBCreate(self,dbcpath):

            try:
                  list_fdbcname=list()
                  for root, dirs, files in os.walk(str(dbcpath)):
                  
                        for name in [name for name in files
                                    if name.endswith((".dbc", ".ldf"))]:
                              fname = os.path.join(root, name)
                              list_fdbcname.append(fname)

                  can_info=MatrixInfo()
                  candbc=can_info.CanMatrixDb(list_fdbcname,self.listmessageboxfile,self.listmessageboxinsert)            
                  return True
            except Exception as e:
                  mymsgbox = traceback.print_exc()
                  self.listmessageboxfile(mymsgbox)
                  return False