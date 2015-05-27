import logging
import time

from button import Button
from relay import Relay

class Humidifier():
  """A Humidifier class."""

  def __init__(self, power_pin, button_pin, name, status=0):
    self.power_relay = Relay(power_pin, name + '_power_relay', 0)
    self.button = Button(button_pin, name + '_button', 0)
    self.status = 0

  def set_status(self, status):
    if status == 0:
      self.power_relay.off()
    else:
      self.power_relay.on()
      self.button.switch_status()

  def on(self):
    # if self.status <> 1:
    self.set_status(1)
    self.status = 1

  def on_for(self, active_time):
    # if self.status <> 1:
    self.on()
    time.sleep(active_time)
    self.off()

  def off(self):
    # if self.status <> 0:
    self.set_status(0)
    self.status = 0

  def get_status(self):
    return self.status
