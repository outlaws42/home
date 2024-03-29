#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Imports ///////////////////
from time import sleep
from datetime import datetime, timedelta, date, time
from pymongo import MongoClient
from bson.codec_options import CodecOptions
import pytz
from helpers.wizard_home import WizardHome #config_exist, config_setup
from helpers.file import FileInfo
from helpers.dict_list import DictList
from helpers.io import IO
from config.conf import conf_dir, conf_file


wh = WizardHome()
fi = FileInfo()
dl = DictList()
io = IO()


# Refresh rate /////////////////////////////////
refresh_type = '1'  # 1 = minutes 2 = Seconds
refresh_rate_amount = 15

if refresh_type == '1':
  # Minutes Refresh (minutes*60) sleep() is in seconds
  refresh = (refresh_rate_amount*60)  
else:
  # Seconds Refresh refresh_rate_amount sleep() is in seconds
  refresh = refresh_rate_amount

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

db_uri = settings['DB_URI']
database = settings['DATABASE']
api = settings['API']
use_api = settings['USE_API']
zip_code = settings['ZIP_CODE']
units = settings['UNITS']

if api == 1:
  from weather.wbit import Weather
elif api == 2:
  from weather.owm import Weather
elif api == 3:
  from weather.weatherapi import Weather

# Database info
mongo = MongoClient(db_uri)
db = mongo[database]

read_collection = 'current'
write_collection = 'past'
key_find = 'updated'
key_sort = 'current_temp'

class GetWeather():
  run_once = 1

  def __init__(self):
    try:
      while True:
       self.main()
       sleep(refresh)
    except (KeyboardInterrupt) as e:
        print(e)
        print('Interupted')
  
  def main(self):
    self.weather = Weather()
    self.weather.get_weather_info(use_api,zip_code,units)
    self.forecast = dl.combine_dict(self.weather.get_forecast())
    self.weather_info = dl.combine_dict(self.weather.gleen_info())
    self.replace_one_db('forecast', self.forecast)
    self.write_one_db('current', self.weather_info)

    # collection read , collection writing, find key, sort key
    self.get_high_low_temp_db(
      read_collection,
      write_collection, 
      key_find, 
      key_sort
      )

  def write_one_db(self, col, data):
    """ write one to a mongoDB database  """
    collection = db[col]
    collection.insert_one(data)
  
  def replace_one_db(self, col, data):
    """ replace one document in a mongoDB database  """
    collection = db[col]
    collection.replace_one({'replace' : 1}, data, True)

  def get_high_low_temp_db(self, coll_read, coll_write, find_key, sort_key):
    """ Gets High and Low temp for the day. only between 11:30pm and 12pm """
    now = datetime.now()
    today12am = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today1230am = now.replace(hour=0, minute=35, second=0, microsecond=0)
    today1130pm = now.replace(hour=23, minute=30, second=0, microsecond=0)
    if now >= today1130pm and self.run_once == 1:
      high_low = self.get_high_low_today(coll_read, find_key, sort_key)
      self.write_one_db(coll_write, high_low)
      self.run_once = 0
    else:
      if today12am <= now <= today1230am:
        self.run_once = 1

  def get_doc_today_db(self, col, key):
    """ Gets Documents from today mongoDB database """
    today = datetime.combine(date.today(), time())
    tomorrow = today + timedelta(1)
    collection = db[col]
    aware_times = collection.with_options(
          codec_options=CodecOptions(tz_aware=True,tzinfo=pytz.timezone('US/Eastern')))
    response = aware_times.find({key :{'$lt' : tomorrow, '$gte' : today}})
    results = [doc for doc in response]
    return results

  def get_high_low_today(self, col,find_key, sort_key):
    today_doc = self.get_doc_today_db(col, find_key)
    temp_list = self.high_low_list(today_doc, sort_key)
    today = datetime.combine(date.today(), time())
    high_low = {
              'icon' : temp_list[0]['current_icon'],
              'high' : temp_list[0]['current_temp'], 
              'low' : temp_list[1]['current_temp'], 
              'date' : today}
    return high_low

  def high_low_list(self, listin, key):
    """ sort list by a key in the dictionaries
        Then get first and last dictionary from the list """
    listout = []
    listin.sort(key=lambda item: item.get(key))
    listout.append(listin[-1])
    listout.append(listin[0])
    return listout

if __name__ == "__main__":
  app = GetWeather()    
