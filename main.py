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
from relay import Relay
from switch import Switch
from temphumid import Temphumid

# Google Docs spreadsheet name.
GDOCS_SPREADSHEET_NAME = 'Temp-umid test'

# Logging
# filepath needs to be an absolute path so that the script run by the root user through crontab can write the logs
LOG_FILEPATH = '/home/pi/salame/logs.log'
logging.basicConfig(
  filename = LOG_FILEPATH,
  level = logging.DEBUG,
  format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class Salame(object):

  def __init__(self):

    try:
      self.main()
    except KeyboardInterrupt:
      print 'exit regularly'
      logging.debug('exit regularly')
      self.exit()
      sys.exit(0)
      raise
    except:
      print 'exception:'
      print traceback.format_exc()
      logging.error(traceback.format_exc())
      raise

  def main(self):
    print 'Salame started'
    logging.debug('Salame started')

    # Create objects
    self.led1 = Led(11, 'LED-yellow-1')
    self.led2 = Led(15, 'LED-yellow-2')
    self.th_sensor = Temphumid(4)
    self.fridge = Relay(12, 'Fridge')
    self.humidifier = Relay(16, 'Humidifier')
    self.data_logger = Google_spreadsheet(GDOCS_SPREADSHEET_NAME)

    self.tmp_test_relay()

    # Create threads
    self.alert_started_worker = threading.Thread(target=self.alert_started)
    self.alert_started_worker.setDaemon(True)
    self.fridge_monitor_worker = threading.Thread(target=self.fridge_monitor)
    self.fridge_monitor_worker.setDaemon(True)

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
    logging.shutdown()


  def fridge_monitor(self):
    while True:
      humidity, temp = self.th_sensor.read()
      if humidity is not None and temp is not None:
        self.led1.blink()
        # print 'Temperature: {0:0.1f} C'.format(temp)
        # print 'Humidity:    {0:0.1f} %'.format(humidity)
        self.data_logger.log([datetime.datetime.now(), temp, humidity])
        time.sleep(5)
      else:
        self.led1.blink_twice()


  def alert_started(self):
    """Turn on red led when the app starts"""
    self.sample_switch = Switch(13, 'LED-red')
    self.sample_switch.on()
    # print "sample_switch status"
    # print self.sample_switch.get_status()
    time.sleep(10)
    self.sample_switch.off()
    # print "sample_switch status"
    # print self.sample_switch.get_status()

  def tmp_test_relay(self):
    self.relay1 = Relay(18, 'relay-1')
    # self.switch2.off()
    for x in range(0, 3):
      self.relay1.on()
      time.sleep(2)
      self.relay1.off()
      time.sleep(2)
    status = self.relay1.get_status()
    print ('relay status:', status)


# init app
app = Salame()
