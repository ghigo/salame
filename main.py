# Salame!

import datetime
import logging
import math
import os.path
import RPi.GPIO as GPIO
import threading
import time
import traceback
import sys

from google_logger import Google_spreadsheet
from button import Button
from humidifier import Humidifier
from led import Led
from relay import Relay
from switch import Switch
from temphumid import Temphumid

# Google Docs spreadsheet name.
GDOCS_SPREADSHEET_NAME = 'salame-logs'

# Logging
# filepath needs to be an absolute path so that the script run by the root user through crontab can write the logs
LOG_FILEPATH = '/home/pi/salame/logs.log'
logging.basicConfig(
  filename = LOG_FILEPATH,
  level = logging.DEBUG,
  format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Settings
# todo: read values from a file
settings = {
  'temperature': 15,
  'temperature_tollerance': 0.5,
  'humidity': 80,
  'humidity_tollerance': 5
}

# Buffer for google spreadsheet logs. Each item is a row (array)
remote_logs = []


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

    # Keep the previous values to evaluate if temp and humid values are increasing or decreasing
    self.prev_t = settings['temperature']
    self.prev_h = settings['humidity']
    # current values
    self.cur_t = 0
    self.cur_h = 0

    # Create objects
    self.led1 = Led(11, 'LED-yellow-1')
    self.led2 = Led(15, 'LED-yellow-2')
    self.th_sensor = Temphumid(4)
    self.fridge = Relay(22, 'Fridge')
    self.humidifier = Humidifier(18, 16, 'Humidifier')
    self.fan = Relay(12, 'Fan')
    self.data_logger = Google_spreadsheet(GDOCS_SPREADSHEET_NAME)

    # self.tmp_test_relay()
    # self.tmp_test_button()
    # self.random()
    # self.tmp_relay()

    # Create threads
    self.alert_started_worker = threading.Thread(target=self.alert_started)
    self.alert_started_worker.setDaemon(True)
    self.fridge_monitor_worker = threading.Thread(target=self.fridge_monitor)
    self.fridge_monitor_worker.setDaemon(True)
    self.logger_worker = threading.Thread(target=self.write_logs)
    self.logger_worker.setDaemon(True)
    # Start threads
    self.alert_started_worker.start()
    self.fridge_monitor_worker.start()
    self.logger_worker.start()

    # keep the app running until all the threads terminate
    while threading.active_count() > 0:
      time.sleep(0.1)


  def exit(self):
    """Cleanup stuff and exit"""
    # Cleanup GPIO
    GPIO.cleanup()
    logging.shutdown()


  def log_values(self, humidity, temperature):
    """
    Format values to log in google spreadsheet

    row:
      time
      humidity
      temperature
      target_humidity
      target_temperature
      humidity tollerance
      temperature tollerance
      fridge status
      fan status
      humidifier status
    """
    print "log_values", datetime.datetime.now()
    row = [datetime.datetime.now(), humidity, temperature, settings['humidity'], settings['temperature'], settings['humidity_tollerance'], settings['temperature_tollerance'], self.fridge.get_status(), self.fan.get_status(), self.humidifier.get_status()]
    # self.data_logger.log(row)
    remote_logs.append(row)


  def fridge_monitor(self):
    """monitor fridge components"""
    while True:
      self.prev_h = self.cur_h
      self.prev_t = self.cur_t
      humidity, temperature = self.th_sensor.read()
      if humidity is not None and temperature is not None:
        self.led1.blink()
        self.cur_h = humidity
        self.cur_t = temperature
        self.control_elements(humidity, temperature)

        # todo put in a separate thread in order not to interrupt the main program in case of failure or delay
        # self.data_logger.log([datetime.datetime.now(), humidity, temperature])
        self.log_values(humidity, temperature);

        # self.fridge_monitor_worker = threading.Thread(target=self.fridge_monitor)
        # self.fridge_monitor_worker.setDaemon(True)

        time.sleep(20)
      else:
        self.led1.blink_twice()

  def write_logs(self):
    while True:
      print "len(remote_logs) = ", len(remote_logs)
      if (len(remote_logs) > 0):
        for x in range(0, len(remote_logs)):
          row = remote_logs.pop(0)
          self.data_logger.log(row)
          print "logger wrote a row"
      time.sleep(30)


  def control_elements(self, humidity, temperature):
    """take decisions based on parameters"""

    # max and min temperatures tollerated
    max_t = settings['temperature'] + settings['temperature_tollerance']
    min_t = settings['temperature'] - settings['temperature_tollerance']
    # temperature
    if temperature >= max_t:
      # Zone A: higher than max
      self.fridge.on()
      print "fridge zone A - on"
    elif temperature <= min_t:
      # Zone D: lower than min
      self.fridge.off()
      print "fridge zone D - off"
    elif (temperature > settings['temperature']) & (temperature < max_t):
      # Zone B: between target and max
      if self.prev_t > temperature:
        # temp decreasing
        self.fridge.off()
        print "fridge zone B - off"
      elif self.prev_t < temperature:
        # temp increasing
        self.fridge.on()
        print "fridge zone B - on"
    elif (temperature < settings['temperature']) & (temperature > min_t):
      # Zone C: between target and min
      if self.prev_t > temperature:
        # temp decreasing
        self.fridge.off()
        print "fridge zone C - off"
      elif self.prev_t < temperature:
        # temp increasing
        self.fridge.on()
        print "fridge zone C - on"
    else:
      print "code should never get here!"


    # humidity
    # if humidity > settings['humidity']:
    #   self.humidifier.off()
    #   self.fan.off()

    if humidity > settings['humidity'] + settings['humidity_tollerance']:
      self.fan.on()
      self.humidifier.off()
      print "humid off"
    elif humidity < settings['humidity'] - settings['humidity_tollerance']:
      self.fan.off()
      humidifier_duration = math.pow(((settings['humidity'] - humidity) / 10 + 1), 3)
      self.humidifier.on_for(humidifier_duration)
      print "humidifier on for ", humidifier_duration
    elif humidity > settings['humidity']:
      self.humidifier.off()
    elif humidity < settings['humidity']:
      self.fan.off()


  def alert_started(self):
    """Turn on red led when the app starts"""
    self.sample_switch = Switch(13, 'LED-red')
    self.sample_switch.on()
    time.sleep(5)
    self.sample_switch.off()








# ------------ TEST

  def tmp_relay(self):
    relay = Relay(12, 'tmp_relay')
    relay.on()
    # relay2 = Relay(22, 'tmp_relay2')
    # relay2.on()
    time.sleep(120)

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
