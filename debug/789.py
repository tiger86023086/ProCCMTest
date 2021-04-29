import can
import time

mybus = can.Bus(bustype='canalystii', channel=0, bitrate=500000)

print(mybus)
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
    msg = mybus.recv()
    if msg is not None:
        print(msg)
    else:
        print(msg)
mybus.shutdown()
