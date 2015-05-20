import logging
import RPi.GPIO as GPIO

class Switch(object):
  """A Switch class"""

  def __init__(self, pin, name, status=0):
    self.pin = pin
    self.name = name
    logging.debug('Switch created - pin: %s, name: %s, status: %s', pin, name, status)

    # Setup GPIO
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, 0)
    self.set_status(status)

  # todo: this should be private
  def set_status(self, status):
    self.status = status
    GPIO.output(self.pin, status)
    logging.debug('switch %s - set_status %s', self.name, status)

  def get_status(self):
    return self.status

  def on(self):
    """Turn on"""
    self.set_status(1)

  def off(self):
    """Turn off"""
    self.set_status(0)
