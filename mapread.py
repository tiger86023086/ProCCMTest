# -*- coding: utf-8 -*-

#  mapread.py
#
#  ~~~~~~~~~~~~
#
#  Function GUI AC Thread
#
#  ~~~~~~~~~~~~
#
#  ------------------------------------------------------------------
#  Author : Li Yonghu
#  Build: 25.04.2021
#  Last change: 25.04.2021 Li Yonghu 
#
#  Language: Python 3.7 
#  ------------------------------------------------------------------
#  GNU GPL
#  
 
#

# Module Imports

import xlrd
import sys

def mapread(filepath,listmessagebox):
    
    wk = xlrd.open_workbook(filepath)
    sheet = wk.sheet_by_index(0)
    map_read_dict = map_dict_create(sheet,listmessagebox)
    
    return map_read_dict

def map_dict_create(sheet,listmessagebox):

    row_num=sheet.nrows
    map_read_dict={}
    loopnum=1

    while loopnum < row_num:

        rowvalue=sheet.row_values(loopnum)
        if rowvalue[1] != '':
            map_read_dict[rowvalue[1]] = [rowvalue[2],rowvalue[5]]
        else:
            pass
        loopnum = loopnum+1
    return map_read_dict

if __name__=='__main__':
    
     filepath = 'E:\\Project\\CCM_Test\\map.xls'
     listmessagebox=''
     error=0
     mapdict = mapread(filepath,listmessagebox)
     print(mapdict)            
        
    
