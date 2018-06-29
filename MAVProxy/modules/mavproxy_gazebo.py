#!/usr/bin/env python

import os
import os.path
import sys
from pymavlink import mavutil
import errno
import time

from socket import *  
from MAVProxy.modules.lib import mp_module
from MAVProxy.modules.lib import mp_util
from MAVProxy.modules.lib import mp_settings

class gazebo(mp_module.MPModule):
	def __init__(self, mpstate):
        """Initialise module"""
        super(example, self).__init__(mpstate, "gazebo", "")
        self.host = '<broadcast>' 
       	#self.BUFSIZE = 512
       	self.port=9011
       	self.frequency=10 #10hz 
       	self.last_send=0
       	
       	self.add_command('set', self.cmd_set, "set",['port'])

       	self.udpCliSock = socket(AF_INET, SOCK_DGRAM)  
		self.udpCliSock.bind(('', 0))  
		self.udpCliSock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1) 

	def usage(self):
        '''show help on command line options'''
        return "Usage: set <port> "
        
	 def idle_task(self):
        '''called rapidly by mavproxy'''
        now = time.time()
        if now-self.last_send > 1000/frequency:
        	addr= (self.host, self.port)
        	self.udpCliSock.sendto(data,addr) 
        	self.last_send=now
        
	def cmd_set(self,args):
		"""set udp broadcast"""
		if len(args)!=2:
			print(self.usage())
		elif args[0]=='port':
			#self.udp_settings.command(args[1:])
			value=int(args[1])
			if value > 65535 or value <2000:
				print(self.usage())
			else:
				self.port=value
		else:
			print(self.usage())
			
	def mavlink_packet(self, m):
        '''handle mavlink packets'''
        #if m.get_type() == 'COMMAND_LONG':
        	
	def unload(self):
        self.udpSerSock.close()  
        
def init(mpstate):
    '''initialise module'''
    return gazebo(mpstate)
