#! /usr/bin/env python3
# -*- coding: utf-8 -*-

version = '2021-04-07'

# Auto text garage door open status
# Requires 4 file .tme, .tme_accum, .cred.yaml, .send
from weather.tmod import open_file, save_file, open_yaml
from pymongo import MongoClient
from config.settings import DB_URI, DATABASE, API
from time import sleep
from os.path import expanduser
import smtplib
import requests
refresh = 60   # In sec.
time_limit_open = 30
time_limit_error = 90
# Database info
mongo = MongoClient(DB_URI)
db = mongo[DATABASE]


class SendMail:
    door_open = 'Open'
    mode = 1  # 0 = Debug mail, 1 = production
    # time_limit = 30  # In min.
    time_increment = 1  # In min.

    def __init__(self):
        self.add_open_time()
        self.logic()
        if self.mode == 0: # debug Mail
            self.mail()
        else:
            pass

    def add_open_time(self):
        c = requests.get('http://192.168.1.3:8000/house/sensors/gdbasement')
        result = c.json()
        sensor_val = result['sensors']['sensor_val']
        if sensor_val == 1:
            self.final_status = 'Closed'
            self.time_limit= time_limit_open
        elif sensor_val == 2:
            self.final_status = 'Open'
            self.time_limit= time_limit_open
        else:
            self.final_status = 'ERROR'
            self.time_limit = time_limit_error
        self.tme = open_file('.tme','home')
        print(f'{self.tme} open from .tme')
        if self.final_status == self.door_open or self.final_status =='ERROR':
            self.tme = int(self.tme)
            self.tme+=self.time_increment
        else:
            self.tme = 0
            self.time_collective = '0'
            save_file('.tme_accum',self.time_collective,'home')
            print(f'{self.time_collective} saving to .tme_accum')
        save_file('.tme',str(self.tme),'home')
        print(f'{self.tme} saving to .tme Limit is {self.time_limit}')

    def logic(self):

        if self.tme >= self.time_limit:
            self.time_collective = open_file('.tme_accum', 'home')
            print(f'{self.time_collective} open from .tme_accum')
            self.time_collective = int(self.time_collective)
            self.time_collective += int(self.tme)
            save_file('.tme_accum', str(self.time_collective), 'home')
            print(f'{self.time_collective} saving to .tme_accum')
            self.mail()
            self.tme = 0
            save_file('.tme', str(self.tme), 'home')

            print('Sending email')
        else:
            pass

    def login_info(self):
        ps = open_yaml('.cred.yaml', 'home')
        for key, value in ps.items():
            us = key
            psw = value
            return [us,psw]

    def mail(self):
        us, psw = self.login_info()
        recipients = open_file('.send', 'home').splitlines()
        content = (
            f'\n Garage: {self.final_status}'
            f'( {self.time_collective} min notifier)'
            )
        subject = 'Garage Door Status'
        message = f'Subject: {subject}\n\n{content}'

        mail = smtplib.SMTP('smtp.gmail.com', 587)

        mail.ehlo()
        mail.starttls()
        mail.ehlo()
        mail.login(us, psw)
        mail.sendmail(us, recipients, message)
        mail.close()


if __name__ == "__main__":
    try:
        while True:
            app = SendMail()
            sleep(refresh)
    except KeyboardInterrupt as e:
        print(e)
        print('Interrupted')
