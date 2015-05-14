# Salame!

import datetime
import time

from google_logger import Google_spreadsheet
from led import Led
from switch import Switch
from temphumid import Temphumid

# Google Docs spreadsheet name.
GDOCS_SPREADSHEET_NAME = 'Temp-umid test'

class Salame(object):

	def __init__(self):
		# main
		print "Welcome to Salame!"
		self.led = Led(11)
		self.th_sensor = Temphumid(4)
		self.data_logger = Google_spreadsheet(GDOCS_SPREADSHEET_NAME)

		self.sample_switch = Switch(13)
		self.sample_switch.on()
		print "sample_switch status"
		print self.sample_switch.get_status()
		time.sleep(2)
		self.sample_switch.off()
		print "sample_switch status"
		print self.sample_switch.get_status()

		# Start monitoring
		self.monitor()


	def monitor(self):
		while True:
			humidity, temp = self.th_sensor.read()
			if humidity is not None and temp is not None:
				self.led.blink()
				print 'Temperature: {0:0.1f} C'.format(temp)
				print 'Humidity:    {0:0.1f} %'.format(humidity)
				self.data_logger.log([datetime.datetime.now(), temp, humidity])
				time.sleep(5)
			else:
				self.led.blink_twice()


	def test(self):

		print "testing..."

		led = Led(11)
		# led.blink(10)
		# led.blink_for(5, 0.15, 0.3)
		led.blink_twice()

		th = Temphumid(4)
		h, t = th.read()
		print t
		print h

		print "Finished testing."

# init app
app = Salame()
