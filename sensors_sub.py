#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Imports ///////////////////
import paho.mqtt.client as mqtt
from datetime import datetime
from pymongo import MongoClient
import time
from config.settings import BROKER_ADDRESS, DB_URI, DATABASE

# Database info
mongo = MongoClient(DB_URI)
db = mongo[DATABASE]

def replace_one_db(col, data, topic,replace):
    """ replace one to a mongoDB database  """
    collection = db[col]
    collection.replace_one({'replace' : replace}, data, True)
    print(f'wrote {topic} to the {col} collection')

def on_message_frtemp(client, userdata, message):
    # Callback fires when a published message is received.
    fr_temp = str(message.payload.decode("utf-8"))
    topic = 'frtemp'
    time_now = datetime.utcnow()
    replace = 2
    t = {
        topic : fr_temp, 
        'dt' : time_now, 
        'replace' : replace
        }
    replace_one_db('sensors', t, topic, replace)
    print(f'Recieved message: {t}')

def on_message_gdstatus(client, userdata, message):
    # Callback fires when a published message is received.
    gd_status = str(message.payload.decode("utf-8"))
    topic = 'gdbasement'
    time_now = datetime.utcnow()
    replace = 1
    t = {
        topic : gd_status, 
        'dt' : time_now, 
        'replace' : replace
        }
    # replace_one_db('sensors', t, topic, replace)
    print(f'Recieved message: {t}')

def on_message(client, userdata, message):
    # Callback fires when a published message is received.

    print(f'Recieved message')

# Create a client and connecting to the broker
client = mqtt.Client('laptop    ')
client.message_callback_add('room/basement/gdstatus',on_message_gdstatus)
client.message_callback_add('room/temperature/front',on_message_frtemp)
client.on_message = on_message
client.connect(BROKER_ADDRESS)
client.subscribe('room/#', 0)
client.loop_forever()

