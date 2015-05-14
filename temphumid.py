import logging
import Adafruit_DHT

class Temphumid(object):
	"""Read temperature and humidity from a DHT22 sensor"""

	sensor = Adafruit_DHT.DHT22

	def __init__(self, pin, name='temphumid'):
		# GPIO pin as marked on board (i.e. use 4 for the 7th pin on the board)
		self.pin = pin
		self.name = name
		logging.debug('Temphumid created - pin: %s, name: %s', pin, name)

	def read(self):
		humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)
		if humidity is None or temperature is None:
			logging.warning('Temphumid %s - Failed to get reading.', self.name)
		logging.debug('Temphumid %s - temperature: %s, humidity: %s', self.name, temperature, humidity)
		return humidity, temperature
