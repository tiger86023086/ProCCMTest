# -*- coding: utf-8 -*-

#  matrixrd.py
#
#  ~~~~~~~~~~~~
#
#  DBC TO DATEBASE(sqlite) API
#
#  ~~~~~~~~~~~~
#
#  ------------------------------------------------------------------
#  Author : Li Yonghu
#  Build:08.04.2021
#  Last change: 09.04.2021 Li Yonghu 
#
#  Language: Python 3.7
#  ------------------------------------------------------------------
#  GNU GPL
#  
 
#

# Module Imports

import sqlite3,os,time

class MatrixInfo:
      def CanMatrixDb(self,dbclist,listmessageboxfile,listmessageboxinsert):
            nodname=''
            msgname=''
            msgid=''
            signame=''
            msb=''
            length=''
            factor=''
            offset=''
            minnum=''
            maxnum=''
            initval='0'
            cycletime='0'
            

            #try:
            filecan = open('CanType.ini')
            cantype_list = filecan.readlines()
            for num in range(len(cantype_list)):
                  cantype_list[num] = cantype_list[num].replace('\n','')

            print(cantype_list)
            #listmessageboxfile.append(cantype_list)

            #tablecan_list = []
            #tablelin_list = []

            if len(dbclist)==0:                  
                  print('There is no Matrix file, Please check ......')
                  messagebox = 'There is no Matrix file, Please check ......'
                  listmessageboxinsert.append(messagebox)
                  return None
            else:
                  npath=os.getcwd()
                  if os.path.exists(npath+'\\Matrix.db'):
                        os.remove(npath+'\\Matrix.db')

                  conn = sqlite3.connect(npath+'\\Matrix.db')
                  cursor = conn.cursor()                  

                  for dbcnum in range(len(dbclist)):                      
                        print(dbclist)
                        dbc_file_name = dbclist[dbcnum]
                        templist = dbclist[dbcnum].split(".")
                        #print templist

                        

                        if templist[-1] == 'dbc':
                              for cantype in cantype_list:
                                    if cantype in dbc_file_name:
                                          tablcanname = cantype
                                          print(tablcanname)
                                          listmessageboxfile.append(tablcanname)
                                          
                                          break
                                    else:
                                          tablcanname = 'CAN_'+str(dbcnum)

                              #tablcanname = 'CAN_'+str(dbcnum)
                              #tablecan_list.append(tablcanname)
                              excu = 'create TABLE '+tablcanname+' (nodename TEXT NOT NULL,messagename TEXT NOT NULL,'+\
                               'messageid TEXT NOT NULL,signalname TEXT NOT NULL,msb TEXT NOT NULL,length TEXT NOT NULL,factor TEXT NOT NULL,\
offset TEXT NOT NULL,minnum TEXT NOT NULL,maxnum TEXT NOT NULL,initval TEXT NOT NULL,cycletime TEXT NOT NULL,CONSTRAINT xh primary key(signalname))'
                              print(excu)
                              listmessageboxfile.append(excu)
                              cursor.execute(excu)                             
                        
                              dbc_content=open(dbc_file_name,'r')            
                              row_content_by_lines = dbc_content.readlines()
                              listnum=0

                              while  listnum <= len(row_content_by_lines)-1:
                                    line=row_content_by_lines[listnum]
                                    if line.find('BO_')==0:
                                        line_temp_list=line.split()
                                        msgname=line_temp_list[2].strip(':')
                                        msgid=hex(int(line_temp_list[1]))
                                        nodname=line_temp_list[4].strip('\n')
                                        listnum=listnum+1
                                        line=row_content_by_lines[listnum]
                                        #signal_list=[]

                                        while line.find(' SG_')==0:
                                            q_pos_l = line.index('|')
                                            q_pos_r = line.rindex('|')
                                            p_pos = line.index('@')
                                            m_pos = line.index(':')
                                            signame = line[5:m_pos-1]
                                            msb = line[m_pos+2:q_pos_l]
                                            length = line[q_pos_l+1:p_pos]


                                            leftparen_pos = line.index('(')
                                            rightparen_pos = line.index(')')
                                            comma_pos = line.index(',')
                                            factor = line[leftparen_pos+1:comma_pos]
                                            offset = line[comma_pos+1:rightparen_pos]


                                            left_zhong = line.index('[')
                                            right_zhong = line.index(']')
                                            minnum = line[left_zhong+1:q_pos_r]
                                            maxnum = line[q_pos_r+1:right_zhong]
                                            list_wrtdb=[nodname,msgname,msgid,signame,msb,length,factor,offset,minnum,maxnum,initval,cycletime]
                                            excu = self.InsertDb(tablcanname,list_wrtdb)
                                            print(excu)
                                            listmessageboxinsert.append(excu)
                                            cursor.execute(excu)
                                            conn.commit()
                                            time.sleep(0.5)
                                            listnum=listnum+1
                                            line=row_content_by_lines[listnum]

                                    elif line.find('BA_ "GenSigStartValue"')==0:
                                          line_temp_list=line.split()
                                          siginitval = line_temp_list[-1].strip(';')
                                          
                                          signalname = line_temp_list[-2]
                                          
                                          excu = "update "+tablcanname+" set initval="+str(siginitval)+" where signalname='"+str(signalname)+"'"
                                          print(excu)
                                          listmessageboxinsert.append(excu)
                                          cursor.execute(excu)
                                          conn.commit()
                                          time.sleep(0.5)
                                          listnum=listnum+1
                                          line=row_content_by_lines[listnum]
                                    elif line.find('BA_ "GenMsgCycleTime"')==0:
                                          line_temp_list=line.split()
                                          sigcycle = line_temp_list[-1].strip(';')
                                          
                                          signalid = line_temp_list[-2]
                                          signalid=hex(eval(signalid))
                                          
                                          excu = "update "+tablcanname+" set cycletime="+str(sigcycle)+" where messageid='"+str(signalid)+"'"
                                          #print excu
                                          listmessageboxinsert.append(excu)
                                          cursor.execute(excu)
                                          conn.commit()
                                          time.sleep(0.5)
                                          listnum=listnum+1
                                          line=row_content_by_lines[listnum]

                                    else:
                                          listnum=listnum+1
                        elif templist[-1] == 'ldf':

                              for cantype in cantype_list:
                                    if cantype in dbc_file_name:
                                          tablinname = cantype
                                          print(tablinname)
                                          listmessageboxfile.append(tablinname)                                                
                                          break
                                    else:
                                          tablinname = 'LIN_'+str(dbcnum)

                              #tablinname = 'LIN_'+str(dbcnum)
                              #tablelin_list.append(tablinname)
                              excu = 'create TABLE '+tablinname+' (messagename TEXT NOT NULL,signalname TEXT NOT NULL,CONSTRAINT xh primary key(signalname))'
                              print(excu)
                              listmessageboxfile.append(excu)
                              cursor.execute(excu)

                              dbc_content=open(dbc_file_name,'r')            
                              row_content_by_lines = dbc_content.readlines()
                              listnum=0
                              
                              flag_strart=0
                              while  listnum != len(row_content_by_lines)-1:
                                    line=row_content_by_lines[listnum]                              

                                    if line.find('Frames')==0:
                                        flag_strart=1
                                        
                                    if flag_strart==1:                        
                                        listnum=listnum+1
                                        line=row_content_by_lines[listnum]
                                        
                                        if line.find('}')!=-1:
                                            flag_strart=0
                                        elif line.find(':') and line.find('{'):
                                            line_temp_list=line.split()
                                            msgname=line_temp_list[0].strip(':')
                                            #print message_name
                                            listnum=listnum+1
                                            line=row_content_by_lines[listnum]
                                            signal_list=[]

                                            while line.find('}')==-1:
                                                signame = line[4:line.index(',')]

                                                list_wrtdb=[msgname,signame]
                                                excu = self.InsertDb(tablinname,list_wrtdb)
                                                print(excu)
                                                listmessageboxinsert.append(excu)
                                                cursor.execute(excu)
                                                conn.commit()
                                                time.sleep(0.5)
                                                
                                                listnum=listnum+1
                                                line=row_content_by_lines[listnum]
                                    else:
                                        listnum=listnum+1

                        else:
                              print(dbc_file_name+' is wrong !!!')
                              messagebox = dbc_file_name+' is wrong !!!'
                              listmessageboxinsert.append(messagebox)

                  cursor.close()
                  conn.close()
                  #return (tablecan_list,tablelin_list)
                  return True
##            except:
##                  return False


      def InsertDb(self,tablname,insert_list):

            reinsert = 'INSERT INTO '+tablname+' VALUES('
            for num in range(len(insert_list)):
                  if num == 0:
                        reinsert = reinsert+"'"+str(insert_list[num])+"'"
                  else:
                        reinsert = reinsert+','+"'"+str(insert_list[num])+"'"

            reinsert = reinsert+')'
            return reinsert

if __name__=='__main__':
      dbclist=['E:\\Project\\CCM_Test\\M891改制冬标车版本_Body.dbc']
      listmessagebox=[]
      listmessageboxinsert=[]
      dbcrd = MatrixInfo()
      dbcrd.CanMatrixDb(dbclist,listmessagebox,listmessageboxinsert)
      
      
