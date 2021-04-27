# -*- coding: utf-8 -*-

#  canalystiiAPI.py
#
#  ~~~~~~~~~~~~
#
#  canalystii(chuangxinkeji CAN box) API
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

import os,time
from ctypes import *
import logging
import platform
from can import Message

logger = logging.getLogger(__name__)

#设备接口类型
VCI_USBCAN1 = 3
VCI_USBCAN2 = 4
VCI_USBCAN2A = 4
VCI_USBCAN_E_U = 20
VCI_USBCAN_2E_U = 21

#函数调用返回状态值
STATUS_OK = 1
STATUS_ERR = 0

TIMING_DICT = {
    5000: (0xBF, 0xFF),
    10000: (0x31, 0x1C),
    20000: (0x18, 0x1C),
    33330: (0x09, 0x6F),
    40000: (0x87, 0xFF),
    50000: (0x09, 0x1C),
    66660: (0x04, 0x6F),
    80000: (0x83, 0xFF),
    83330: (0x03, 0x6F),
    100000: (0x04, 0x1C),
    125000: (0x03, 0x1C),
    200000: (0x81, 0xFA),
    250000: (0x01, 0x1C),
    400000: (0x80, 0xFA),
    500000: (0x00, 0x1C),
    666000: (0x80, 0xB6),
    800000: (0x00, 0x16),
    1000000: (0x00, 0x14),
}

#定义初始化CAN的数据类型
class VCI_INIT_CONFIG(Structure):  
    _fields_ = [("AccCode", c_ulong),
                ("AccMask", c_ulong),
                ("Reserved", c_ulong),
                ("Filter", c_ubyte),
                ("Timing0", c_ubyte),
                ("Timing1", c_ubyte),
                ("Mode", c_ubyte)
                ]
#定义CAN信息帧的数据类型
class VCI_CAN_OBJ(Structure):  
    _fields_ = [("ID", c_uint),
                ("TimeStamp", c_uint),
                ("TimeFlag", c_ubyte),
                ("SendType", c_ubyte),
                ("RemoteFlag", c_ubyte),#是否是远程帧
                ("ExternFlag", c_ubyte),#是否是扩展帧
                ("DataLen", c_ubyte),
                ("Data", c_ubyte*8),
                ("Reserved", c_ubyte*3)
                ]
cwdpath = os.getcwd()
os.chdir(cwdpath)

try:
    if platform.system() == "Windows":
        CANalystII = WinDLL("./ControlCAN.dll")
    else:
        CANalystII = CDLL("./libcontrolcan.so")
    logger.info("Loaded CANalystII library")
except OSError as e:
    CANalystII = None
    logger.info("Cannot load CANalystII library")

class CANalystIIBus:
    def __init__(
        self,
        channel,
        device=0,
        bitrate=None,
        Timing0=None,
        Timing1=None,
        can_filters=None,
        **kwargs,
    ):
        """

        :param channel: channel number
        :param device: device number
        :param bitrate: CAN network bandwidth (bits/s)
        :param Timing0: customize the timing register if bitrate is not specified
        :param Timing1:
        :param can_filters: filters for packet
        """

        if isinstance(channel, (list, tuple)):
            self.channels = channel
        elif isinstance(channel, int):
            self.channels = [channel]
        else:
            # Assume comma separated string of channels
            self.channels = [int(ch.strip()) for ch in channel.split(",")]

        self.device = device

        self.channel_info = "CANalyst-II: device {}, channels {}".format(
            self.device, self.channels
        )

        if bitrate is not None:
            try:
                Timing0, Timing1 = TIMING_DICT[bitrate]
            except KeyError:
                raise ValueError("Bitrate is not supported")

        if Timing0 is None or Timing1 is None:
            raise ValueError("Timing registers are not set")

        self.init_config = VCI_INIT_CONFIG(0x80000008, 0xFFFFFFFF, 0, 2, Timing0, Timing1, 0)

        ret = 0
        ret = CANalystII.VCI_OpenDevice(VCI_USBCAN2, self.device, 0)
        time.sleep(5)
        

        if ret == STATUS_ERR:
            logger.error("VCI_OpenDevice Error")

        for channel in self.channels:
            status = CANalystII.VCI_InitCAN(
                VCI_USBCAN2, self.device, channel, byref(self.init_config)
            )
            time.sleep(5)
            if status == STATUS_ERR:
                logger.error("VCI_InitCAN Error")
                self.shutdown()
                return
        
            ret = 0
            ret = CANalystII.VCI_StartCAN(VCI_USBCAN2, self.device, channel)
            time.sleep(5)

            if CANalystII.VCI_StartCAN(VCI_USBCAN2, self.device, channel) == STATUS_ERR:
                logger.error("VCI_StartCAN Error")
                self.shutdown()
                return
    def sendmsg(self, msg, timeout=None):
        """

        :param msg: message to send
        :param timeout: timeout is not used here
        :return:
        """
        extern_flag = 1 if msg.is_extended_id else 0
        raw_message = VCI_CAN_OBJ(
            msg.arbitration_id,
            0,
            0,
            1,
            msg.is_remote_frame,
            extern_flag,
            msg.dlc,
            (c_ubyte * 8)(*msg.data),
            (c_ubyte * 3)(0, 0, 0),
        )

        if msg.channel is not None:
            channel = msg.channel
        elif len(self.channels) == 1:
            channel = self.channels[0]
        else:
            raise ValueError("msg.channel must be set when using multiple channels.")
        
        CANalystII.VCI_Transmit(
            VCI_USBCAN2, self.device, channel, byref(raw_message), 1
        )
        
    def recvmsg(self, timeout=None):
        """

        :param timeout: float in seconds
        :return:
        """
        raw_message = VCI_CAN_OBJ(0x0, 0, 0, 1, 0, 0,  8,(c_ubyte * 8)(*msg.data),(c_ubyte * 3)(0, 0, 0),)

        timeout = -1 if timeout is None else int(timeout * 1000)

        status = CANalystII.VCI_Receive(
            VCI_USBCAN2, self.device, self.channels[0], byref(raw_message), 1, timeout
        )
        time.sleep(5)
        print(status)
        if status <= STATUS_ERR:
            return None, False
        else:
            return (
                Message(
                    timestamp=raw_message.TimeStamp if raw_message.TimeFlag else 0.0,
                    arbitration_id=raw_message.ID,
                    is_remote_frame=raw_message.RemoteFlag,
                    channel=0,
                    dlc=raw_message.DataLen,
                    data=raw_message.Data,
                ),
                False,
            )

    def flush_tx_buffer(self):
        for channel in self.channels:
            CANalystII.VCI_ClearBuffer(VCI_USBCAN2, self.device, channel)
            
    def shutdown(self):
        CANalystII.VCI_CloseDevice(VCI_USBCAN2, self.device)

if __name__=='__main__':
        from can import Message
        
        mycan = CANalystIIBus(0,device=0,bitrate=500000)
        #msg = Message()
        msg = Message(data=[1,2,3,4,5,6,7,8],dlc = 8,arbitration_id = 0x100,channel = 0)
        
        mycan.sendmsg(msg,timeout=None)

        
##        recmsg = mycan.recvmsg(timeout=1)
##        print(recmsg[0])
##        
        
        
        
        
        

