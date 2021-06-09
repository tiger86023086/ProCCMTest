from basic import *
pcan=PCANBasic()
status=pcan.Initialize(PCAN_USBBUS1,PCAN_BAUD_500K)
print(status)

####write message#####
#######
#Message which has be send display RX??,but VCU has postive response
#######
Msg=TPCANMsg()
Msg.LEN=c_ubyte(8)
Msg.MSGTYPE=PCAN_MESSAGE_STANDARD
Msg.ID=c_ulong(int('0x7b0',16))
Msg.DATA=(c_ubyte(int('0x03',16)),c_ubyte(int('0x22',16)),c_ubyte(int('0xf1',16)),c_ubyte(int('0x93',16)),c_ubyte(int('0x0',16)),c_ubyte(int('0x0',16)),c_ubyte(int('0x0',16)),c_ubyte(int('0x0',16)))
result=pcan.Write(PCAN_USBBUS1,Msg)

####remove hardware####
pcan.Uninitialize(PCAN_USBBUS1)
