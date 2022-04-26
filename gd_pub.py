#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from helpers.io import IO
# Imports ///////////////////
import paho.mqtt.client as mqtt
import time
from helpers.wizard_home import WizardHome
from helpers.file import FileInfo
from helpers.html_tools import HT
from config.conf import conf_dir, conf_file
from helpers.io import IO

wh = WizardHome()
fi = FileInfo()
io = IO()
ht = HT()


try:
  file_exists = fi.check_file_dir(
    fname = f"{conf_dir}/{conf_file}",
    fdest = "home"
    )
  if file_exists == False:
      wh.config_setup(conf_dir, conf_file)
  else:
     settings = io.open_settings(conf_dir, conf_file)
except Exception as e:
      print(e)

# Create a client and connecting to the broker
mqtt_broker = settings['BROKER_ADDRESS']
client = mqtt.Client('garage_door')
client.connect(mqtt_broker)

# Publish to the broker
while True:
    garage_door = settings['GARAGE_DOOR_ADDRESS']
    final_status = ht.html_info('b',f'http://{garage_door}:8080')
    client.publish('room/basement/gdstatus', final_status)
    # print(f'Just Published {final_status} to topic room/basement/gdstatus')
    time.sleep(10)

