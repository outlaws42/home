#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import FastAPI
from bson import json_util
from pymongo import MongoClient
import json
# from bson.codec_options import CodecOptions
# from datetime import datetime, timedelta, date, time
# from config.settings import DB_URI,DATABASE
from config.conf import conf_dir, conf_file
from helpers.wizard_rest import config_exist, config_setup, open_settings
from helpers import (get_certain_dated_entry_db, get_latest_with_tz_db, 
     check_for_delay_time, list_collection_with_tz_db,get_latest_named_with_tz_db, 
     put_in_dict, timestamp_from_datetime)

# Init app
app = FastAPI()

try:
  file_exists = config_exist(conf_dir, conf_file)
  if file_exists == False:
      print(file_exists)
      config_setup(conf_dir, conf_file)
  else:
    settings = open_settings(conf_dir, conf_file)
except Exception as e:
      print(e)

db_uri = settings['DB_URI']
database = settings['DATABASE']

# Database
mongo = MongoClient(db_uri)
db = mongo[database]


@app.get('/')
def index():
  return 'Home API (See /docs for information on the API)'

@app.get('/weather/{collection}')
def weather(collection: str):
  if (collection  == 'current' or 
    collection == 'forecast' or 
    collection == 'indoor' or 
    collection == 'sensors'):
    if collection == 'current':
      date_key = 'updated'
      root_key = 'current'
    elif collection == 'forecast':
      date_key = 'date'
      root_key = 'forecast'
  else:
    return 404
  result = get_latest_with_tz_db(db, collection)
  date_stamp = timestamp_from_datetime(result[0][date_key])
  dict = put_in_dict(root_key, date_key, result, date_stamp)
  sterilized = json.loads(json_util.dumps(dict))
  return sterilized

@app.get('/weather/past/{history}')
def weather_history(history: str):
    print(history)
    if history == 'day' or history == 'year':
      if history == 'year':
        days = 365 #517
      elif history == 'day':
        days = 1
      else:
        days = 0
    else:
      return f'404 ${history}'
    try:
      result = get_certain_dated_entry_db(db,'past', days)
      print(f'High_Low Result: {result}')
      date_stamp = timestamp_from_datetime(result[0]['date'])
      dict = put_in_dict(f'forecast_{history}', 'date', result, date_stamp)
    except:
      dict = {f'forecast_{history}':{'icon': 0, 'high': 0, 'low': 0,  'date' : 0}}
    sterilized = json.loads(json_util.dumps(dict))
    return sterilized

@app.get('/house/sensors')
def sensors():
  date_key = 'dt'
  root_key = 'sensors'
  result = list_collection_with_tz_db(db, 'sensors')
  # date_stamp = timestamp_from_datetime(result[0][date_key])
  # dict = put_in_dict(root_key, date_key, result, date_stamp)
  # check_for_indoor_negative(dict, root_key,'front_room')
  # check_for_delay_time(dict, root_key, date_key, name)
  # sterilized = json.loads(json_util.dumps(dict))
  return result

@app.get('/house/sensors/{name}')
def sensors(name:str):
  date_key = 'dt'
  root_key = 'sensors'
  result = get_latest_named_with_tz_db(db, root_key,name)
  print(result[0][date_key])
  date_stamp = timestamp_from_datetime(result[0][date_key])
  dict = put_in_dict(root_key, date_key, result, date_stamp)
  # check_for_indoor_negative(dict, root_key,'front_room')
  check_for_delay_time(dict, root_key, date_key, 'sensor_val')
  sterilized = json.loads(json_util.dumps(dict))
  return sterilized

# Run Server
# if __name__ == "__main__":
#     app.run(debug=True, port=5000, host='0.0.0.0')
