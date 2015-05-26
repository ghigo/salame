import logging
import RPi.GPIO as GPIO
import time

from relay import Relay

class Button(Relay):
  """A Button class implemented using a relay. It gives an on/off short input to turn the button ON and the same input to turn it OFF"""

  def __init__(self, pin, name, status=0):
  	self.button_status = 0
  	super(Button, self).__init__(pin, name, status)

  def _super_on(self):
  	return super(Button, self).on()

  def _super_off(self):
  	super(Button, self).off()

  def switch_status(self):
  	self._super_on()
  	time.sleep(0.2)
  	self._super_off()

 	def on(self):
 		if (self.button_status == 0):
 			self.switch_status()

	def off(self):
		if (self.button_status <> 0):
			self.switch_status()

	def get_status(self):
		return self.button_status
