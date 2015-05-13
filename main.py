# Salame!

from led import Led
from temphumid import Temphumid
import time

class Salame(object):

	def __init__(self):
		# main
		print "Welcome to Salame!"
		self.led = Led(11)
		self.th_sensor = Temphumid(4)

		# Start monitoring
		self.monitor()


	def monitor(self):
		while True:
			humidity, temp = self.th_sensor.read()
			self.led.blink()
			print 'Temperature: {0:0.1f} C'.format(temp)
			print 'Humidity:    {0:0.1f} %'.format(humidity)
			time.sleep(5)



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
