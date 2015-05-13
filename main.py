# Salame!

from led import Led

class Salame(object):

	def __init__(self):
		# main
		print "Welcome to Salame!"

		led = Led(11)
		# led.blink(10)
		# led.blink_for(5, 0.15, 0.3)
		led.blink_twice()


# init app
app = Salame()
