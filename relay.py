import logging
import RPi.GPIO as GPIO

from switch import Switch

class Relay(Switch):
  """Relay class. A relay gives power when off"""

  def set_status(self, status):
    # invert the status
    return super(Relay, self).set_status(not status)

  def get_status(self):
    # invert the status
    return not super(Relay, self).get_status()
