#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Imports ///////////////////
import paho.mqtt.client as mqtt
import time
from helpers.html_tools import HT
from config.conf import conf_dir, conf_file
from helpers.io import IO

io = IO()
ht = HT()

# Get config
settings = io.open_settings(conf_dir, conf_file)

# Create a client and connecting to the broker
mqtt_broker = settings['BROKER_ADDRESS']
client = mqtt.Client('garage_door')
client.connect(mqtt_broker)

# Publish to the broker
while True:
    final_status = ht.html_info('b','http://192.168.1.24:8080')
    client.publish('room/basement/gdstatus', final_status)
    # print(f'Just Published {final_status} to topic room/basement/gdstatus')
    time.sleep(10)

