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
import os ,sys,sqlite3
from ctypes import *

class mysignal :
    def __init__(self):
        self.ID = 0
        self.MSGNAME = ''
        self.SIGNALNAME = ''
        self.MSB = 0
        self.LEN = 0
        self.FACTOR = 0
        self.OFFSET = 0
    
    

def signal2bit(signal,msb,slen):

    bitboard=[0,8,16,24,32,40,48,56,7,15,23,31,39,47,55,63]
    bitarray=[0,0,0,0,0,0,0,0]

    for i in range(8):
        if msb <= bitboard[i+8] and slen<=8:
            shiftval = msb+1-slen-bitboard[i]
            if shiftval >= 0:
                afshiftval = signal>>shiftval
                
            elif shiftval < 0:
                afshiftval = signal<<abs(shiftval)
            else:
                print('shiftvalue is none!')

            temp_value = afshiftval+bitarray[i]
            bitarray[i] = temp_value & 255
            break
        
        elif msb<=bitboard[i+8] and slen>8 and slen<=16:
            shiftval = -(slen-(8-(bitboard[i+8]-msb)))

            if shiftval >= 0:
                afshiftval = signal >> shiftval
            elif shiftval < 0:                
                afshiftval = signal >> abs(shiftval)
            else:
                print('shiftvalue is none!')
        
            temp_value = afshiftval+bitarray[i]
            bitarray[i] = temp_value & 255

            shiftval1 = 8+shiftval
            if shiftval1 >= 0:
                afshiftval1 = signal << shiftval1
            elif shiftval1 < 0:                
                afshiftval1 = signal << abs(shiftval1)
            else:
                print('shiftvalue1 is none!')

            temp_value1 = afshiftval1+bitarray[i+1]
            bitarray[i+1] = temp_value1 & 255
            
            break
        else:
            print('length more than 16!')

    return bitarray

def bit2signal(msb,slen,bitarray):

    bitboard=[0,8,16,24,32,40,48,56,7,15,23,31,39,47,55,63]
    signal = 0

    for i in range(8):
         if msb <= bitboard[i+8] and slen<8:
            shiftval = msb-slen-bitboard[i]+1
            if shiftval >= 0:
                afshiftval = bitarray[i] >> shiftval
            else:
                print('Error!')
            signal = afshiftval & (2**slen-1)
            break
         elif msb<=bitboard[i+8] and slen>8 and slen<=16:
            shiftval = slen-(8-(bitboard[i+8]-msb))
            
            if shiftval >= 0:
                afshiftval = bitarray[i] << shiftval
            else:
                print('Error!')

            signal = signal + afshiftval

            shiftval1 = 8-shiftval
            if shiftval1 >= 0:
                afshiftval1 = bitarray[i+1] >> shiftval1
            else:
                print('Error!')
            
            signal = signal + afshiftval1

            break
         else:
            print('length more than 16!')

    return signal            
    

def list_postion(signal,flag_bc):
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
              excu = "select messageid,messagename,msb,length,factor,offset from "+tablename+" where signalname='"+signal+"'"
              cursor.execute(excu)

              temp_list = cursor.fetchall()
              if temp_list:
                  signalstru.ID = temp_list[0][0]
                  signalstru.MsgName = temp_list[0][1]
                  signalstru.MSB = temp_list[0][2]
                  signalstru.LEN = temp_list[0][3]
                  signalstru.FACTOR = temp_list[0][4]
                  signalstru.OFFSET = temp_list[0][5]
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

    aa=list_postion('CCM_CcmBmsReqAcPower',1)
    mysigmsb = eval(aa.MSB)
    print(mysigmsb)
    mysiglen = eval(aa.LEN)
    print(mysiglen)
    cc = signal2bit(550,mysigmsb,mysiglen)
    print(cc)#0,0,0,2,26,0,0,0

    mybitarra = [0,0,0,2,26,0,0,0]
    dd = bit2signal(28,13,mybitarra)
    print(dd)

    
    

 
