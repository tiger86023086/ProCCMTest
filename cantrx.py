# -*- coding: utf-8 -*-

#  cantrx.py
#
#  ~~~~~~~~~~~~
#
#  Function GUI AC Thread
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

import sys
import can
import time

class cantrx:
    def initcan(self,bustype,channel,bitrate):
        try:
            self.mybus = can.Bus(bustype=bustype, channel=channel,
                                 bitrate=bitrate)
            if self.mybus == None:
                print('Cannot open device!')
                sys.exit()
        except:
            self.mybus = can.Bus(bustype=bustype, channel=channel,
                                 bitrate=bitrate)
            if self.mybus == None:
                print('Cannot open device!')
                sys.exit()
    def sendmsg(self,mymsg):
        try:
            self.mybus.send(mymsg)
        except:
            self.mybus.send(mymsg)

    def sendmsgperiod(self,mymsg,period):
        try:
            task = self.mybus.send_periodic(mymsg,period,store_task=True)
            #print(task)
            #assert isinstance(task,can.broadcastmanager.CyclicSendTaskABC)
            if task == None:
                print('Cannot send message period')
                return task
                sys.exit()
            return task
        except:
            pass
            # task = self.mybus.send_periodic(mymsg,period,store_task=True)
            # #assert isinstance(task, can.CyclicSendTaskABC)
            # return task
    def stopsendperiod(self):
        try:
            self.mybus.stop_all_periodic_tasks()

        except:
            self.mybus.stop_all_periodic_tasks()
    def recvmsg(self):
        try:
            mymsg = self.mybus.recv()
            print(mymsg)
            if mymsg == None:
                mymsg = self.mybus.recv(timeout=0.001)
        except:
            mymsg=None
##            mymsg = self.mybus.recv(timeout=0.01)
            pass
        return mymsg
    
    def clustermsg(self,datadict,cycdict,channel):

        listmymsg = []
        
        myiterdata = iter(datadict)
        while True:
            try:
                mydictkey = next(myiterdata)
                msgdata = datadict[mydictkey]
                msgcyc = eval(cycdict[mydictkey])
                
                mymsg = can.Message(arbitration_id = eval(mydictkey),
                                    is_extended_id=False,
                                    data = msgdata,dlc =8,
                                    channel = channel)
                listmymsg.append([mymsg,msgcyc])
            except StopIteration:
                
                break
        return listmymsg

    def mysendmsgp(self,listmymsg):
        
           for mylist in listmymsg:
               mymsg = mylist[0]
               mycycle = mylist[1]
               self.sendmsgperiod(mymsg,mycycle)
               
            
    def delcan(self):
        self.mybus.shutdown()
        
if __name__=='__main__':
    import time
    import signalbit

    # mycan = signalbit.canconvert()

    # mycan.initcandb('E:\\Project\\CCM_Test\\M891改制冬标车版本_Body.dbc')
    # mysigdata,myid = mycan.encodemsg({'IVI_BlowerLvlSet':7,'IVI_CCMDrvTempSet':32,
    #                                   'IVI_HourSet':12,'ESP_VehicleSpeed':20})

    # mysigdata1,myid1 = mycan.encodemsg({'IVI_BlowerLvlSet':2,'IVI_CCMDrvTempSet':32,
    #                                   'IVI_HourSet':12,'ESP_VehicleSpeed':20})
    
    mycantrx = cantrx()
    mycantrx.initcan('neovi',1,500000)

    while True:
        try:
            canrecvmsg = mycantrx.recvmsg()
            print(canrecvmsg.arbitration_id)
        except:
            pass

    mycantrx.delcan()

##    mymessage = can.Message(arbitration_id=0x400, is_extended_id=False,
##                      data=[2,2,3,4,5,6,7,8],dlc = 8,
##                      channel = 0)
##    mymessage1 = can.Message(arbitration_id=0x410, is_extended_id=False,
##                      data=[1,2,3,4,5,6,7,8],dlc = 8,
##                      channel = 0)
##    #mycantrx.sendmsg(mymessage)
##    aa = mycantrx.sendmsgperiod(mymessage,0.01)
##    bb = mycantrx.sendmsgperiod(mymessage1,0.1)
##    print(aa)
##    print(bb)
##    time.sleep(100)
#     mylistmsg = mycantrx.clustermsg(mysigdata,myid)
#     mylistmsg1 = mycantrx.clustermsg(mysigdata1,myid1)
#     tasks={}
    
#     for msg in mylistmsg:
        
#         mymsg = msg[0]
#         print(type(mymsg))
#         mycycle = float(msg[1]/1000)
#         print(type(mycycle))
#         tasks[mymsg] = mycantrx.sendmsgperiod(mymsg,mycycle)
#         #counter =counter + 1
#         print(tasks)

#     for i in range(5):

#         for msg in mylistmsg1:
            
#             mymsg = msg[0]
#             mycantrx.sendmsg(mymsg)
#             time.sleep(0.01)
            
# ##            print(type(mymsg))
# ##            mycycle = float(msg[1]/1000)
# ##            print(type(mycycle))
# ##            tasks[mymsg] = mycantrx.sendmsgperiod(mymsg,mycycle)
# ##            #counter =counter + 1
# ##            print(tasks)
    
       
#                #assert isinstance(task, can.CyclicSendTaskABC)
    
#     #mycantrx.mysendmsgp(mylistmsg)
#     time.sleep(100)

#     for tkey in list(tasks.keys()):
#         tasks[tkey].stop()
#         time.sleep(5)
# ##    mycantrx.stopsendperiod()
# ##    time.sleep(10)
#     mycantrx.delcan()
