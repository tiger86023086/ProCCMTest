# -*- coding: utf-8 -*-

#  signalbit.py
#
#  ~~~~~~~~~~~~
#
#  Function signal2bit bit2signal
#
#  ~~~~~~~~~~~~
#
#  ------------------------------------------------------------------
#  Author : Li Yonghu
#  Build: 09.04.2021
#  Last change: 09.04.2021 Li Yonghu 
#
#  Language: Python 3.7
#  ------------------------------------------------------------------
#  GNU GPL
#  
 
#

# Module Imports
import os
import sys
import sqlite3

import cantools

class mysignal :
    def __init__(self):
        self.ID = 0
        self.MSGNAME = ''
        self.SIGNALNAME = ''
        self.MSB = 0
        self.LEN = 0
        self.FACTOR = 0
        self.OFFSET = 0
        self.INITVALUE = 0
        self.CYCLE = 0

        
class canconvert():
     def initcandb(self,dbfile):
         
         self.mydb = cantools.database.load_file(dbfile)
     def _encodemsg(self,dict_signals,msgname):
         if msgname == None:
             print('Message name is none')
             return None
         else:
             mymsg = self.mydb.get_message_by_frame_id(eval(msgname))
             print(dict_signals)
             mydata = mymsg.encode(dict_signals)
             return mydata

     def decodemsg(self,msgid,msgdata):
        mydictsig = self.mydb.decode_message(msgid,msgdata,decode_choices=False)
        return mydictsig
    
     def idserach(self,listsig):

        listid = list()

        myiter = iter(listsig)        
        while True:
            try:
                mysignal = next(myiter)
                sigdetail = self.list_postion(mysignal,1)

                if sigdetail !=None:
                    mymsgid = eval(sigdetail.ID)                    
                else:
                    print('cannot find the signal--%s',mysignal)
                    sys.exit()
                if mymsgid != '':
                    if not mymsgid in listid:

                        listid.append(mymsgid)
                
            except StopIteration:
                
                break
            
            
        return listid        
     def encodemsg(self,dict_signals):
        mydict = {}
        mydatadict={}
        mycycdict = {}
        mymsgname = ''
        #sigdetail = signalbit.mysignal()
        
        myiter = iter(dict_signals)
        
        while True:
            try:
                mysignal = next(myiter)
                sigdetail = self.list_postion(mysignal,1)

                if sigdetail !=None:
                    mymsgname = sigdetail.ID
                    mymsgcycle = sigdetail.CYCLE
                else:
                    print('cannot find the signal--%s',mysignal)
                    sys.exit()

                if mymsgname != '':
                
                    if mymsgname in list(mydict.keys()):
                        mydictsig = mydict[mymsgname]
                        mydictsig.update({mysignal:dict_signals[mysignal]})
                        mydict[mymsgname]=mydictsig

                        mycycdict[mymsgname] = mymsgcycle

                        
                    elif not mymsgname in list(mydict.keys()):
                        mydictsig={mysignal:dict_signals[mysignal]}
                        mydict[mymsgname]=mydictsig

                        mycycdict[mymsgname] = mymsgcycle
                         
                    else:
                        print('The dictionary signals is not in any message!')
                        break
                else:
                    print('The dictionary signals is not in any message!')
                        
                    break
            except StopIteration:
                
                break

        for msg in list(mydict.keys()):
            sigdict = mydict[msg]
            sigother = self.mydb.get_message_by_frame_id(eval(msg))
            for signal in sigother.signals:
                signame = signal.name

                if signame in sigdict.keys():
                    pass
                elif not signame in sigdict.keys():
                    
                    sigdetail = self.list_postion(signame,1)
##                    print(sigdetail.INITVALUE)
##                    print(sigdetail.FACTOR)
##                    print(sigdetail.OFFSET)
                    signalinitval = eval(sigdetail.INITVALUE)*eval(sigdetail.FACTOR)+eval(sigdetail.OFFSET)
                    sigdict.update({signame:signalinitval})
##                    print(signame)
##                    print(signalinitval)
                else:
                    print('Unknown Error!!')
            mydict[msg] = sigdict
        
        for msg in list(mydict.keys()):
            
            mydict_signals = mydict[msg]
            mydata = self._encodemsg(mydict_signals,msg)
            mydatadict[msg] = mydata
            #mydatadict[msg] = mydata.hex()
        return mydatadict,mycycdict               

        
     def list_postion(self,signal,flag_bc):
      #flag_bc:1--CLN  0--BUS
        signalstru = mysignal()
        signalstru.SignalName = signal
        flag_find = 0

        conn = sqlite3.connect('Matrix.db')
        cursor = conn.cursor()

        cursor.execute("select name from sqlite_master where type='table'")
        tablename_list = cursor.fetchall()
        #table_list = []
        for table in tablename_list:
            tablename = str(table[0])
            if flag_bc == 1:
                  excu = "select messageid,messagename,msb,length,factor,offset,initval,cycletime from "+tablename+" where signalname='"+signal+"'"
                  cursor.execute(excu)

                  temp_list = cursor.fetchall()
                  if temp_list:
                      signalstru.ID = temp_list[0][0]
                      signalstru.MsgName = temp_list[0][1]
                      signalstru.MSB = temp_list[0][2]
                      signalstru.LEN = temp_list[0][3]
                      signalstru.FACTOR = temp_list[0][4]
                      signalstru.OFFSET = temp_list[0][5]
                      signalstru.INITVALUE = temp_list[0][6]
                      signalstru.CYCLE = temp_list[0][7]
                      flag_find = 1                
                      break
                  else:
                      pass
            if flag_bc == 0:
                  excu = "select * from "+tablename+" where messagename='"+signal+"'"
                  cursor.execute(excu)

                  temp_list = cursor.fetchall()
                  if temp_list:
                      flag_find = 1
                      msgname = signal
                      break
                  else:
                        pass

        if flag_find:
            return (signalstru)
        else:
            return (None)

        cursor.close()
        conn.close()
         
if __name__=='__main__':
    mycan = canconvert()
    
    #aa=mycan.list_postion('CCM_CcmBmsReqAcPower',1)
    mycan.initcandb('E:\\Project\\CCM_Test\\M891改制冬标车版本_Body.dbc')

##    #encoding debug
##    #mysigdata,myid = mycan.encodemsg({'IVI_BlowerLvlSet':7,'IVI_CCMDrvTempSet':32})
##    mysigdata,myid = mycan.encodemsg({'IVI_BlowerLvlSet':7,'IVI_CCMDrvTempSet':32,'IVI_HourSet':12})
##    print(mysigdata,myid)

    #decoding debug
    mylist  = mycan.idserach(['IVI_BlowerLvlSet','IVI_CCMDrvTempSet','ESP_VehicleSpeed'])
    print(mylist)
    
