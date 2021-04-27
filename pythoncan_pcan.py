import can

mybus = can.Bus(bustype='pcan', channel='PCAN_USBBUS1', bitrate=500000)
mymessage = can.Message(arbitration_id=0x400, is_extended_id=False,
                      data=[1,2,3,4,5,6,7,8],dlc = 8,
                      channel = 0)
mybus.send(mymessage,timeout=None)

mybus.shutdown()
