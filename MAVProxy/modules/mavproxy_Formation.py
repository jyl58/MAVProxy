#!/usr/bin/env python

"""LCM type definitions
This file automatically generated by lcm.
DO NOT MODIFY BY HAND!!!!
"""
try:
    import cStringIO.StringIO as BytesIO
except ImportError:
    from io import BytesIO
import struct

class pos_info_t(object):
    __slots__ = ["timestamp", "lat", "lon", "alt", "relative_alt", "vx", "vy", "vz", "head"]

    __typenames__ = ["int64_t", "int32_t", "int32_t", "int32_t", "int32_t", "int16_t", "int16_t", "int16_t", "int16_t"]

    __dimensions__ = [None, None, None, None, None, None, None, None, None]

    def __init__(self):
        self.timestamp = 0
        self.lat = 0
        self.lon = 0
        self.alt = 0
        self.relative_alt = 0
        self.vx = 0
        self.vy = 0
        self.vz = 0
        self.head = 0

    def encode(self):
        buf = BytesIO()
        buf.write(pos_info_t._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        buf.write(struct.pack(">qiiiihhhh", self.timestamp, self.lat, self.lon, self.alt, self.relative_alt, self.vx, self.vy, self.vz, self.head))

    def decode(data):
        if hasattr(data, 'read'):
            buf = data
        else:
            buf = BytesIO(data)
        if buf.read(8) != pos_info_t._get_packed_fingerprint():
            raise ValueError("Decode error")
        return pos_info_t._decode_one(buf)
    decode = staticmethod(decode)

    def _decode_one(buf):
        self = pos_info_t()
        self.timestamp, self.lat, self.lon, self.alt, self.relative_alt, self.vx, self.vy, self.vz, self.head = struct.unpack(">qiiiihhhh", buf.read(32))
        return self
    _decode_one = staticmethod(_decode_one)

    _hash = None
    def _get_hash_recursive(parents):
        if pos_info_t in parents: return 0
        tmphash = (0x757d804b4649f3a) & 0xffffffffffffffff
        tmphash  = (((tmphash<<1)&0xffffffffffffffff) + (tmphash>>63)) & 0xffffffffffffffff
        return tmphash
    _get_hash_recursive = staticmethod(_get_hash_recursive)
    _packed_fingerprint = None

    def _get_packed_fingerprint():
        if pos_info_t._packed_fingerprint is None:
            pos_info_t._packed_fingerprint = struct.pack(">Q", pos_info_t._get_hash_recursive([]))
        return pos_info_t._packed_fingerprint
    _get_packed_fingerprint = staticmethod(_get_packed_fingerprint)

'''cmd to fllower'''
class command_t(object):
    __slots__ = ["command"]

    __typenames__ = ["int16_t"]

    __dimensions__ = [None]

    def __init__(self):
        self.command = 0

    def encode(self):
        buf = BytesIO()
        buf.write(command_t._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        buf.write(struct.pack(">h", self.command))

    def decode(data):
        if hasattr(data, 'read'):
            buf = data
        else:
            buf = BytesIO(data)
        if buf.read(8) != command_t._get_packed_fingerprint():
            raise ValueError("Decode error")
        return command_t._decode_one(buf)
    decode = staticmethod(decode)

    def _decode_one(buf):
        self = command_t()
        self.command = struct.unpack(">h", buf.read(2))[0]
        return self
    _decode_one = staticmethod(_decode_one)

    _hash = None
    def _get_hash_recursive(parents):
        if command_t in parents: return 0
        tmphash = (0x304d4fab5f291c2c) & 0xffffffffffffffff
        tmphash  = (((tmphash<<1)&0xffffffffffffffff) + (tmphash>>63)) & 0xffffffffffffffff
        return tmphash
    _get_hash_recursive = staticmethod(_get_hash_recursive)
    _packed_fingerprint = None

    def _get_packed_fingerprint():
        if command_t._packed_fingerprint is None:
            command_t._packed_fingerprint = struct.pack(">Q", command_t._get_hash_recursive([]))
        return command_t._packed_fingerprint
    _get_packed_fingerprint = staticmethod(_get_packed_fingerprint)


"""
status to qgc
"""
class status_t(object):
    __slots__ = ["sysid"]

    __typenames__ = ["int16_t"]

    __dimensions__ = [None]

    def __init__(self):
        self.sysid = 0

    def encode(self):
        buf = BytesIO()
        buf.write(status_t._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        buf.write(struct.pack(">h", self.sysid))

    def decode(data):
        if hasattr(data, 'read'):
            buf = data
        else:
            buf = BytesIO(data)
        if buf.read(8) != status_t._get_packed_fingerprint():
            raise ValueError("Decode error")
        return status_t._decode_one(buf)
    decode = staticmethod(decode)

    def _decode_one(buf):
        self = status_t()
        self.sysid = struct.unpack(">h", buf.read(2))[0]
        return self
    _decode_one = staticmethod(_decode_one)

    _hash = None
    def _get_hash_recursive(parents):
        if status_t in parents: return 0
        tmphash = (0xa686a4dbe27ada97) & 0xffffffffffffffff
        tmphash  = (((tmphash<<1)&0xffffffffffffffff) + (tmphash>>63)) & 0xffffffffffffffff
        return tmphash
    _get_hash_recursive = staticmethod(_get_hash_recursive)
    _packed_fingerprint = None

    def _get_packed_fingerprint():
        if status_t._packed_fingerprint is None:
            status_t._packed_fingerprint = struct.pack(">Q", status_t._get_hash_recursive([]))
        return status_t._packed_fingerprint
    _get_packed_fingerprint = staticmethod(_get_packed_fingerprint)


"""
    Formation conmunication mavproxy module
    independ: lcm
"""
import sys
from pymavlink import mavutil
import errno
import time
import math
import threading
import os
import lcm

from MAVProxy.modules.lib import mp_module
from MAVProxy.modules.lib import mp_util
from MAVProxy.modules.lib import mp_settings
class Formation(mp_module.MPModule):
    def __init__(self, mpstate):
        """Initialise module"""
        super(Formation, self).__init__(mpstate, "Formation", "formation control")
        self._lcm=None
        self._is_leader=False
        self._sub_pos=None
        self._sub_cmd=None
        self._handle_thread=None
        self._should_pub_leader_msg=False
        print("Init the Formation module")

    def mavlink_packet(self, msg):
        '''handle a mavlink packet'''
        if msg.get_type()=="HEARTBEAT":
            if msg.get_srcSystem()==1:
                self._is_leader=True
                '''unsub the channel on leader'''
                if self._lcm and self._sub_pos:
                    self._lcm.unsubscribe(self._sub_pos)
                    self._sub_pos=None

                if  self._lcm and self._sub_cmd:
                    self._lcm.unsubscribe(self._sub_cmd)
                    self._sub_cmd=None
            else:
                self._is_leader=False
                if self._lcm and not self._sub_pos:
                    print("Sub the formation's topic")
                    self._sub_pos=self._lcm.subscribe("Leader_Pos", self.handleLeaderPos)
                    self._sub_cmd=self._lcm.subscribe("Command", self.handleCommand)
                    self._handle_thread = threading.Thread(target=self.lcmHandleThread)
                    self._handle_thread.daemon = True
                    self._handle_thread.start()
            '''pub link msg to qgc'''
            if self._lcm:
                state=status_t()
                state.sysid=msg.get_srcSystem()
                self._lcm.publish("STATUS",state.encode())

        elif msg.get_type()=="SERVO_OUTPUT_RAW":
            if not self._is_leader:
                return
            
            if (msg.servo1_raw>1500 and msg.servo3_raw <1500 and math.abs(msg.servo1_raw)==math.abs(msg.servo3_raw)) or(msg.servo1_raw<1500  and msg.servo3_raw >1500 and math.abs(msg.servo1_raw)==math.abs(msg.servo3_raw)) or(msg.servo1_raw==1500  and msg.servo3_raw ==1500) or (msg.servo1_raw<1500 and msg.servo3_raw <1500):
                self._should_pub_leader_msg=False
            else:
                self._should_pub_leader_msg=True

        elif msg.get_type()=="GLOBAL_POSITION_INT":
            if not self._is_leader:
                return

            if self.get_mav_param("FOLL_ENABLE")==None:
                print("Waiting param download complete.")
                return 
            if int(self.get_mav_param("FOLL_ENABLE"))==0:
                print("Formation operator is not enable,if need please use qgc open it.")
                return

            pos_info=pos_info_t()
            pos_info.timestamp=msg.time_boot_ms
            pos_info.lat  = msg.lat   #degE7
            pos_info.lon  = msg.lon   #degE7
            pos_info.alt  = msg.alt   #alt
            pos_info.relative_alt=msg.relative_alt
            pos_info.vx   = msg.vx    #cm/s
            pos_info.vy   = msg.vy    #cm/s
            pos_info.vz   = msg.vz    #cm/s
            pos_info.head = msg.hdg   #deg*100
            # leader's command to follow
            command=command_t()
            if self._lcm:
                print("timestamp="+str(pos_info.timestamp))
                #multicast the leader's info
                if not self._should_pub_leader_msg: 
                    command.command=0  #0 is hold the follower
                    print("leader is not move, pub cmd set the follower to hold mode: "+str(command.command))
                else:
                    command.command=1
                    print("Pub leader's lat="+str(pos_info.lat)+"; lon="+str(pos_info.lon)+"; vx="+str(pos_info.vx)+"cm/s; vy="+str(pos_info.vy)+"cm/s"+"; head="+str(pos_info.head))
                    self._lcm.publish("Leader_Pos",pos_info.encode())

                self._lcm.publish("Command",command.encode())
            else:
                print("lcm is None")


    def lcmHandleThread(self):
        if not self._lcm:
            print("lcm is None")
            return
        try:
            while True:
                self._lcm.handle()
        except KeyboardInterrupt:
            print("lcm handle except")


    def handleLeaderPos(self,channel, data):
        if channel != "Leader_Pos":
            return

        lcm_msg = pos_info_t.decode(data)
        print("Sub leader's location info:")
        print("timestamp="+str(lcm_msg.timestamp))
        print("lat="+str(lcm_msg.lat)+"; lon="+str(lcm_msg.lon)+"; vx="+str(lcm_msg.vx)+"cm/s; vy="+str(lcm_msg.vy)+"cm/s"+"; head="+str(lcm_msg.head))
        #send msg to flight control
        self.master.mav.global_position_int_send(
            lcm_msg.timestamp,   # time_boot_ms ()
            lcm_msg.lat,    
            lcm_msg.lon,   #leader current location 
            lcm_msg.alt,  # alt 
            lcm_msg.relative_alt,  #relative alt
            #leader current velocity cm/s
            lcm_msg.vx,
            lcm_msg.vy,
            lcm_msg.vz, 
            lcm_msg.head    # head 
            )

    def handleCommand(self,channel, data):
        if channel != "Command":
            return

        '''check formation param'''
        if self.get_mav_param("FOLL_ENABLE")==None:
            print("Waiting param download complete.")
            return

        if int(self.get_mav_param("FOLL_ENABLE"))==0:
            print("This MAV does not open formation operator,pleae open it if need")
            return

        cmd=command_t.decode(data)
        print("leader's command "+str(cmd.command))
        if cmd.command==0:
            if self.master and self.status.flightmode != "HOLD" and self.status.flightmode != "MANUAL":
                mode_mapping = self.master.mode_mapping()
                self.master.set_mode(mode_mapping["HOLD"])
        elif cmd.command==1:
            if self.master and self.status.flightmode != "FOLLOW" and self.status.flightmode != "MANUAL":
                mode_mapping = self.master.mode_mapping()
                self.master.set_mode(mode_mapping["FOLLOW"])


    def idle_task(self):
        if self._lcm==None:
            ip=os.popen('hostname -I').read().splitlines()[0]
            if len(ip)>0:
                print("init the lcm")
                self._lcm=lcm.LCM("udpm://224.0.0.84:58661?ttl=1")

     
def init(mpstate):
    '''initialise module'''
    return Formation(mpstate)
        
    
        
