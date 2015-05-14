# Salame!

import datetime
import logging
import os.path
import RPi.GPIO as GPIO
import threading
import time
import traceback
import sys

from google_logger import Google_spreadsheet
from led import Led
from switch import Switch
from temphumid import Temphumid

# Google Docs spreadsheet name.
GDOCS_SPREADSHEET_NAME = 'Temp-umid test'

# Logging
LOG_FILEPATH = 'logs.log'
logging.basicConfig(
  filename = LOG_FILEPATH,
  level = logging.DEBUG,
  format = '%(asctime)s %(message)s')


class Salame(object):

  def __init__(self):

    try:
      self.main()
    except KeyboardInterrupt:
      logging.debug('exit regularly')
      self.exit()
      sys.exit(0)
      raise
    except:
      logging.error(traceback.format_exc())
      raise

  def main(self):
    logging.debug('Salame started')

    # Create objects
    self.led = Led(11)
    self.th_sensor = Temphumid(4)
    self.data_logger = Google_spreadsheet(GDOCS_SPREADSHEET_NAME)

    # Create threads
    self.alert_started_worker = threading.Thread(target=self.alert_started)
    self.alert_started_worker.setDaemon(True)
    self.fridge_monitor_worker = threading.Thread(target=self.fridge_monitor)
    self.fridge_monitor_worker_.setDaemon(True)

    # Start threads
    self.alert_started_worker.start()
    self.fridge_monitor_worker.start()

    # keep the app running until all the threads terminate
    while threading.active_count() > 0:
      time.sleep(0.1)


  def exit(self):
    """Cleanup stuff and exit"""
    # Cleanup GPIO
    GPIO.cleanup()


  def fridge_monitor(self):
    while True:
      humidity, temp = self.th_sensor.read()
      if humidity is not None and temp is not None:
        self.led.blink()
        print 'Temperature: {0:0.1f} C'.format(temp)
        print 'Humidity:    {0:0.1f} %'.format(humidity)
        self.data_logger.log([datetime.datetime.now(), temp, humidity])
        time.sleep(5)
      else:
        self.led.blink_twice()


  def alert_started(self):
    """Turn on red led when the app starts"""
    self.sample_switch = Switch(13)
    self.sample_switch.on()
    print "sample_switch status"
    print self.sample_switch.get_status()
    time.sleep(10)
    self.sample_switch.off()
    print "sample_switch status"
    print self.sample_switch.get_status()


  def test(self):
    print "testing..."

    led = Led(11)
    # led.blink(10)
    # led.blink_for(5, 0.15, 0.3)
    led.blink_twice()

    th = Temphumid(4)
    h, t = th.read()
    print t
    print h

    print "Finished testing."

# init app
app = Salame()
