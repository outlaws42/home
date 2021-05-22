#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# from bson.codec_options import CodecOptions
import pytz
from collections import ChainMap
from datetime import datetime, timedelta, date, time
from helpers.dt import DT 

dt = DT()


# def timestamp_from_datetime(dt):
#     """ Convert Datetime to timestamp """
#     timestamp_ = int(dt.timestamp())
#     return timestamp_


# def str_date_from_datetime(datetime_):
#     str_date = datetime_.strftime('%Y-%m-%d')
#     return str_date


def put_in_dict(root_key, date_key, in_list, date_stamp):
    dict = {root_key: {}}
    for key in in_list[0]:
        dict[root_key][key] = in_list[0][key]
    dict[root_key][date_key] = date_stamp
    print(dict)
    return dict


# def combine_dict(dict_list):
#     """
#     Takes a list of dictionarys and combines into one dictionary
#     requires from collections import ChainMap and python 3.3 or later
#     """
#     current = dict(ChainMap(*dict_list))
#     print(f'combine_dict {current}')
#     return current


def check_for_indoor_negative(dictionary, root_key, key):
    """
    Checks checks to see if the temp is negative if so it makes it 0
    """
    if dictionary[root_key][key] < 0:
        print('NEGATIVE NUMBER')
        dictionary[root_key][key] = 0
        print(dictionary)
    return dictionary


def check_for_delay_time(dictionary, root_key, date_key, name_key):
    """
    Checks to see how much time between now
    and when the last write to the db
    if to long then sets to 0
    """
    time_stamp = dictionary[root_key][date_key]
    # value_type = type(dictionary[root_key][name_key])
    # print(f"Name Key Type: {value_type}")
    now = datetime.now()
    then = datetime.fromtimestamp(time_stamp)
    tdelta = now - then
    seconds = tdelta.total_seconds()
    minute = 60
    print(f"timeDelta: {tdelta}")
    print(f"seconds: {seconds}")
    if seconds >= minute:
      dictionary[root_key][name_key] = 0
    # elif seconds >= minute and value_type == str:
    #   dictionary[root_key][name_key] = 'NR'
    print(f"{root_key} Dictionary after time check {dictionary}")
    return dictionary


def get_latest_with_tz_db(db, col_read):
    """ Gets latest document by _id mongoDB database with 
       local timezone return list with latest document"""
    collection = db[col_read]
    aware_times = collection.with_options(
        codec_options=CodecOptions(tz_aware=True, tzinfo=pytz.timezone('US/Eastern')))
    response = aware_times.find({}, {'_id': 0, 'replace': 0}).sort("_id", -1).limit(1)
    results = [doc for doc in response]
    return results

def list_collection_with_tz_db(db, col_read):
    """ Gets latest document by _id mongoDB database with 
       local timezone return list with latest document"""
    collection = db[col_read]
    aware_times = collection.with_options(
        codec_options=CodecOptions(tz_aware=True, tzinfo=pytz.timezone('US/Eastern')))
    response = aware_times.find({}, {'_id': 0, 'replace' :0}).sort("_id", -1)
    results = [doc for doc in response]
    return results


def get_latest_named_with_tz_db(db, col_read,name):
    """ Gets latest document by _id mongoDB database with 
       local timezone return list with latest document"""
    collection = db[col_read]
    aware_times = collection.with_options(
        codec_options=CodecOptions(tz_aware=True, tzinfo=pytz.timezone('US/Eastern')))
    # if name == 'gdbasement':
    #   response = aware_times.find({:{'$in':['Open','Closed']}}, {'_id': 0, 'replace' : 0}).sort("_id", -1).limit(1)
    # else:
    response = aware_times.find({'sensor':{'$in':[name]}}, {'_id': 0}).sort("_id", -1).limit(1)
    results = [doc for doc in response]
    print(f'get_multi {results}')
    return results


def get_certain_dated_entry_db(db, col, past):
    """ Gets past document by date from today mongoDB 
        database with return list with past document"""
    past_days = datetime.combine(
        date.today(),
        time()) - timedelta(past)
    past_days_plus_one = past_days + timedelta(1)
    collection = db[col]
    response = collection.find({
        'date': {'$lt': past_days_plus_one,
                 '$gte': past_days}}, {'icon': 1, 'high': 1, 'low': 1, 'date': 1, '_id': 0}).sort('_id', -1).limit(1)
    result = [doc for doc in response]
    return result
