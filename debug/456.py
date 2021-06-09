import can
import time
mybus = can.interface.Bus(bustype="pcan",channel="PCAN_USBBUS1",bitrate=500000)
#bus = can.interface.Bus(bustype='pcan', channel='PCAN_USBBUS1', bitrate=500000)

##print(mybus)
##mymessage = can.Message(arbitration_id=0x400, is_extended_id=False,
##                      data=[1,2,3,4,5,6,7,8],dlc = 8,
##                      channel = 0)
##aa = mybus.send(mymessage)
##print(aa)
##bb = mybus.send_periodic(mymessage,0.1)
##print(bb)
##time.sleep(10)
##mybus.stop_all_periodic_tasks()
##time.sleep(1000)
while True:
    for i in range(4):
        msg = mybus.recv()
        if msg is not None:
            print(msg)
            print(msg.arbitration_id)
            print(type(msg.arbitration_id))
            if msg.arbitration_id == 838:
                print('yes')
            if msg.arbitration_id == 839:
                print('yes1')
            if msg.arbitration_id == 837:
                print('yes2')
            if msg.arbitration_id == 0x340:
                print('yes3')



##else:
##    print(msg)
mybus.shutdown()
