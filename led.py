import RPi.GPIO as GPIO
import time

DURATION_VERY_SHORT = 0.2
DURATION_SHORT = 0.5
DURATION_NORMAL = 1

class Led(object):
	"""An LED class"""

	def __init__(self, pin):
		self.pin = pin

		# Setup GPIO
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(pin, GPIO.OUT)

	def blink(self, duration=DURATION_NORMAL):
		"""Blink once"""
		print 'Led blink'
		GPIO.output(self.pin, True)
		time.sleep(duration)
		GPIO.output(self.pin, False)

	def blink_for(self, times=10, light=DURATION_NORMAL, sleep=DURATION_NORMAL):
		"""Blink specifying time, light duration and sleep duration"""
		for x in range(0, times):
			self.blink(light)
			time.sleep(sleep)

	def blink_twice(self):
		"""Blink twice"""
		self.blink_for(2, DURATION_VERY_SHORT, DURATION_VERY_SHORT)
