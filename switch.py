import RPi.GPIO as GPIO

class Switch(object):
	"""A Switch class"""

	def __init__(self, pin):
		self.pin = pin
		self.status = 0

		# Setup GPIO
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(pin, 0)

	# todo: this should be private
	def set_status(self, status):
		self.status = status
		GPIO.output(self.pin, status)

	def get_status(self):
		return self.status

	def on(self):
		"""Turn on"""
		self.set_status(1)

	def off(self):
		"""Turn off"""
		self.set_status(0)
