import logging
import setinterval
import time

from button import Button
from relay import Relay

class Humidifier():
  """A Humidifier class."""

  def __init__(self, power_pin, button_pin, name, status=0):
    self.power_relay = Relay(power_pin, name + '_power_relay', 0)
    self.button = Button(button_pin, name + '_button', 0)
    self.status = 0
    # self.nominal_status = 0
    # 0 = Off - 1 = On - 2 = on for - 3 = pulse
    self.advanced_status = 0
    # active, pause time. It is valid only if self.status = 1
    self.status_interval = []
    # Interval used to activate the component after a certain time
    self.interval = None

  def get_status(self):
    # convert to boolean
    return not(not self.advanced_status)

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
    self.advanced_status = 1

  def on_for(self, active_time):
    logging.debug('Humidifier on_for: %s', active_time)
    self.on()
    time.sleep(active_time)
    self.off()
    self.advanced_status = 1

  def pulse(self, active_time, sleep):
    set_interval(on_for)

  def off(self):
    self.set_status(0)
    self.status = 0
    self.advanced_status = 0

