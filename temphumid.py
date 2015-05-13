import Adafruit_DHT

class Temphumid(object):
	"""Read temperature and humidity from a DHT22 sensor"""

	sensor = Adafruit_DHT.DHT22

	def __init__(self, pin):
		# GPIO pin as marked on board (i.e. use 4 for the 7th pin on the board)
		self.pin = pin

	def read(self):
		humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)
		if humidity is None or temperature is None:
			print 'Temphumid: Failed to get reading. Try again!'
		return humidity, temperature
