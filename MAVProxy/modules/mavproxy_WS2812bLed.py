import os
import os.path
import sys
from pymavlink import mavutil
import errno
import time

#import ws2812 control lib
from luma.led_matrix.device import ws2812
from luma.core.render import canvas

from MAVProxy.modules.lib import mp_module
from MAVProxy.modules.lib import mp_util
from MAVProxy.modules.lib import mp_settings

class WS2812bLed(mp_module.MPModule):
	def __init__(self, mpstate):
        """Initialise module"""
        super(WS2812bLed, self).__init__(mpstate, "WS2812bLed", "")
		self.ws2812_dev=ws2812(cascaded=4)
		self.status_led_addr=range(0,4);
		self.vehicle_status="empty"
		self.last_status_update=time.time()
		self.led_status_light=False
		self.status_led_color={'empty':(0,0,0),'ACTIVE':"green",'STANDBY':"blue",'CRITICAL':"yellow"}
		
	def mavlink_packet(self, m):
		'''handle mavlink packets'''
		if m.get_type()=="HEARTBEAT":
			if m.system_status==5 or m.system_status==6:
				self.vehicle_status="CRITICAL"
			elif m.system_status==3:
				self.vehicle_status="ACTIVE"
			elif m.system_status==4:
				self.vehicle_status="ACTIVE"
						
	def status_led(self):
	 	'''status led '''
        now = time.time()
        if now-self.last_status_update > 0.5: # s
        	self.last_status_update=now
        	if not self.led_status_light:
            	self.led_status_light=True
            	with canvas(self.ws2812_dev) as draw:
                	for i in self.status_led_addr:
                    	draw.point((i, 0), fill=self.status_led_color[self.vehicle_status])
            else:
            	self.led_status_light=False
                with canvas(self.ws2812_dev) as draw:
                	for i in self.status_led_addr:
                    	draw.point((i, 0), (0, 0, 0))

	def idle_task(self):
		'''control led by status'''
		self.status_led()

def init(mpstate): 
    '''initialise module'''
    return WS2812bLed(mpstate)
