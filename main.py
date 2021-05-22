#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import FastAPI
from bson import json_util
from pymongo import MongoClient
import json
from config.conf import conf_dir, conf_file
from helpers.wizard_home import WizardHome
from helpers.file import FileInfo
from helpers.io import IO
from helpers.dt import DT
from helpers import (get_certain_dated_entry_db, get_latest_with_tz_db, 
     check_for_delay_time, list_collection_with_tz_db,get_latest_named_with_tz_db, 
     put_in_dict)

# init helper classes
wh = WizardHome()
fi = FileInfo()
io = IO()
dt = DT()

# Init app
app = FastAPI()

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
  date_stamp = dt.from_datetime(
    dt = result[0][date_key], 
    timestamp = True
    )
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
      date_stamp = dt.from_datetime(
    dt = result[0]['date'], 
    timestamp = True
    )
      dict = put_in_dict(f'forecast_{history}', 'date', result, date_stamp)
    except:
      dict = {f'forecast_{history}':{'icon': 0, 'high': 0, 'low': 0,  'date' : 0}}
    sterilized = json.loads(json_util.dumps(dict))
    return sterilized

@app.get('/house/sensors')
def sensors():
  result = list_collection_with_tz_db(db, 'sensors')
  return result

@app.get('/house/sensors/{name}')
def sensors(name:str):
  date_key = 'dt'
  root_key = 'sensors'
  result = get_latest_named_with_tz_db(db, root_key,name)
  print(result[0][date_key])
  date_stamp = dt.from_datetime(
    dt = result[0][date_key], 
    timestamp = True
    )
  dict = put_in_dict(root_key, date_key, result, date_stamp)
  check_for_delay_time(dict, root_key, date_key, 'sensor_val')
  sterilized = json.loads(json_util.dumps(dict))
  return sterilized

if __name__ == "__main__":
  pass
#     app.run(debug=True, port=5000, host='0.0.0.0')
