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
from button import Button
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
  # filename = LOG_FILEPATH,
  level = logging.DEBUG,
  format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

settings = {
  'temperature': 25,
  'temperature_tollerance': 2,
  'humidity': 50,
  'humidity_tollerance': 5
}


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
    self.humidifier = Button(16, 'Humidifier')
    self.fan = Relay(12, 'Fan')
    self.data_logger = Google_spreadsheet(GDOCS_SPREADSHEET_NAME)

    # self.tmp_test_relay()
    # self.tmp_test_button()
    # self.random()

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
        self.control_elements(humidity, temp)

        # todo put in a separate thread in order not to interrupt the main program in case of failure or delay
        self.data_logger.log([datetime.datetime.now(), temp, humidity])
        # self.fridge_monitor_worker = threading.Thread(target=self.fridge_monitor)
        # self.fridge_monitor_worker.setDaemon(True)

        time.sleep(5)
      else:
        self.led1.blink_twice()


  def control_elements(self, humid, temp):
    if temp > settings['temperature'] + settings['temperature_tollerance']:
      self.fridge.on()
      print "fridge on"
    elif temp < settings['temperature'] - settings['temperature_tollerance']:
      self.fridge.off()
      print "fridge off"

    if humid > settings['humidity'] + settings['humidity_tollerance']:
      self.fan.on()
      self.humidifier.off()
      print "humid off"
    elif settings['humidity'] - settings['humidity_tollerance']:
      self.fan.off()
      self.humidifier.on()
      print "humid on"


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








# ------------ TEST

  def random(self):
    self.fan1 = Relay(12, 'Fan')
    self.fan1.on()
    self.led3 = Switch(13, 'Led3')
    self.led3.on()


  def tmp_test_button(self):
    self.button1 = Button(16, 'button-1')
    for x in range(0, 100):
      self.button1.on()
      time.sleep(5)
      self.button1.off()
      time.sleep(5)


  def tmp_test_relay(self):
    self.relay1 = Relay(12, 'relay-1')
    # self.switch2.off()
    for x in range(0, 100):
      self.relay1.on()
      time.sleep(0.2)
      self.relay1.off()
      time.sleep(2)
      # self.relay1.off()
      # time.sleep(2)
    status = self.relay1.get_status()
    print ('relay status:', status)


# init app
app = Salame()
