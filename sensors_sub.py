#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Imports ///////////////////
import paho.mqtt.client as mqtt
from datetime import datetime
from pymongo import MongoClient
import time
from helpers.wizard_home import WizardHome #config_exist, config_setup, open_settings
from helpers.file import FileInfo
from helpers.io import IO
from config.conf import conf_dir, conf_file

wh = WizardHome()
fi = FileInfo()
io = IO()

try:
  file_exists = fi.check_file_dir(
    fname = f"{conf_dir}/{conf_file}",
    fdest = "home"
    )
  if file_exists == False:
      print(file_exists)
      wh.config_setup(conf_dir, conf_file)
  else:
     settings = io.open_settings(conf_dir, conf_file)
except Exception as e:
      print(e)

db_uri = settings['DB_URI']
database = settings['DATABASE']
broker_address = settings['BROKER_ADDRESS']

# Database info
mongo = MongoClient(db_uri)
db = mongo[database]

def replace_one_db(col, data, topic):
    """ replace one to a mongoDB database  """
    collection = db[col]
    collection.replace_one({'sensor' : topic}, data, True)
    print(f'wrote {topic} to the {col} collection')

def on_message_frtemp(client, userdata, message):
    # Callback fires when a published message is received.
    fr_temp = int(round(float(message.payload.decode("utf-8"))))
    topic = 'frtemp'
    time_now = datetime.utcnow()
    t = {
        'sensor': topic,
        'sensor_val' : fr_temp, 
        'dt' : time_now, 
        }
    replace_one_db('sensors', t, topic)
    print(f'Recieved message: {t}')

def on_message_gdstatus(client, userdata, message):
    # Callback fires when a published message is received.
    gd_payload = str(message.payload.decode("utf-8"))
    gd_status = 0
    topic = 'gdbasement'
    time_now = datetime.utcnow()
    if gd_payload == 'Closed':
        gd_status = 1
    elif gd_payload == 'Open':
        gd_status = 2

    t = {
        'sensor': topic,
        'sensor_val' : gd_status, 
        'dt' : time_now, 
        }
    replace_one_db('sensors', t, topic)
    print(f'Recieved message: {t}')

def on_message(client, userdata, message):
    # Callback fires when a published message is received.

    print(f'Recieved message')

# Create a client and connecting to the broker
client = mqtt.Client('server')
client.message_callback_add('room/basement/gdstatus',on_message_gdstatus)
client.message_callback_add('room/temperature/front',on_message_frtemp)
client.on_message = on_message
client.connect(broker_address)
client.subscribe('room/#', 0)
client.loop_forever()

