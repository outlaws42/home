#! /usr/bin/env python3
# -*- coding: utf-8 -*-

version = '2021-05-11'

# Auto text garage door open status
# Requires 4 file .open_time, .open_time_accum, .cred.yaml, .send
# from helpers.tmod import (
#   open_file, save_file, open_yaml, 
#   check_dir, mail, decrypt_login,
#   check_file_dir
#   )
from helpers.wizard_automl import (
  config_setup, open_settings, automl_config_exist
  )
from helpers.io import IO as io
from helpers.email import Mail as ml
from helpers.encrypt import Encryption as en
from time import sleep
from requests import get

refresh = 60   # In sec.
time_limit_open = 30
time_limit_error = 90
door_open = 'Open'
mode = 1  # 0 = Debug mail, 1 = production
time_increment = 1  # In min.
conf_dir = '.config/home'
conf_file = 'settings.yaml'
open_time_file = f'{conf_dir}/.open_time'
accum_file = f'{conf_dir}/.open_time_accum'

def add_open_time():
    c = get('http://192.168.1.3:8000/house/sensors/gdbasement')
    result = c.json()
    sensor_val = result['sensors']['sensor_val']
    if sensor_val == 1:
        final_status = 'Closed'
        time_limit= time_limit_open
    elif sensor_val == 2:
        final_status = 'Open'
        time_limit= time_limit_open
    else:
        final_status = 'ERROR'
        time_limit = time_limit_error
    open_time = io.open_file(open_time_file,'home')
    print(f'{open_time} open from .open_time')
    if final_status == door_open or final_status =='ERROR':
        open_time = int(open_time)
        open_time+=time_increment
    else:
        open_time = 0
        time_collective = '0'
        io.save_file(accum_file,time_collective,'home')
        print(f'{time_collective} saving to .open_time_accum')
    io.save_file(open_time_file,str(open_time),'home')
    print(f'{open_time} saving to .open_time Limit is {time_limit}')
    logic(open_time, time_limit, final_status)

def logic(
  open_time: str, 
  time_limit: int,
  final_status: str
  ):
    if open_time >= time_limit:
        time_collective = io.open_file(accum_file, 'home')
        print(f'{time_collective} open from .open_time_accum')
        time_collective = int(time_collective)
        time_collective += int(open_time)
        io.save_file(accum_file, str(time_collective), 'home')
        print(f'{time_collective} saving to .open_time_accum')
        mail_info = mail_info(final_status,time_collective)
        ml.mail(
          body = mail_info['body'], 
          subject = mail_info['subject'], 
          send_to = mail_info['sendto'],
          login = mail_info['login']
        )
        open_time = 0
        io.save_file(open_time_file, str(open_time), 'home')

        print('Sending email')
    else:
        pass

def mail_info(
  final_status: str,
  time_collective: int
  ):
  kf = f"{conf_dir}/.info.key"
  ef = f"{conf_dir}/.cred_en.yaml"
  st = open_settings(conf_dir, conf_file)
  body = (
    f'\n Garage: {final_status}'
    f'( {time_collective} min notifier)'
  )
  sub = 'Garage Door Status'
  key = io.open_file(
    fname = kf, 
    fdest = "home",
    mode ="rb"
    )
  login = en.decrypt_login(
    key = key, 
    e_fname = ef, 
    fdest = "home"
    )
  return {
    "login": login, 
    "body": body, 
    "subject": sub, 
    "sendto": st
    }

def main():
  add_open_time()
  if mode == 0: # debug Mail
    mail_i = mail_info("Closed Test", 30)
    ml.mail(
      body = mail_i['body'], 
      subject = mail_i['subject'], 
      send_to = mail_i['sendto'],
      login = mail_i['login']
        )
  else:
    pass

if __name__ == "__main__":
    try:
        file_exists = automl_config_exist(conf_dir, conf_file)
        if file_exists == False:
          print(file_exists)
          config_setup(conf_dir, conf_file)
        while True:
            app = main()
            sleep(refresh)
    except KeyboardInterrupt as e:
        print(e)
        print('Interrupted')
