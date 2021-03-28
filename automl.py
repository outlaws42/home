#! /usr/bin/env python3

# -*- coding: utf-8 -*-
# Auto text garage door open status
# Requires 3 file .tme, .tme_accum, .cred.json, .send
from weather.tmod import open_file, save_file, open_json
from pymongo import MongoClient
from config.settings import DB_URI, DATABASE, API
from helpers import get_latest_named_with_tz_db
from time import sleep
from os.path import expanduser
import smtplib
refresh = 60   # In sec.

# Database info
mongo = MongoClient(DB_URI)
db = mongo[DATABASE]


class SendMail:
    version = '2021-03-27_1'
    # home = expanduser("~")
    door_open = 'Open'
    mode = 1  # 0 = Debug mail, 1 = production
    time_limit = 30  # In min.
    time_increment = 1  # In min.

    def __init__(self):
        self.add_open_time()
        self.logic()
        if self.mode == 0: # debug Mail
            self.mail()
        else:
            pass

    def add_open_time(self):
        result = get_latest_named_with_tz_db(db, 'sensors','gdbasement')
        sensor_val = result[0]['sensor_val']
        if sensor_val == 1:
            self.final_status = 'Open'
        elif sensor_val == 0:
            self.final_status = 'Closed'
        self.tme = open_file('.tme','home')
        print(str(self.tme) + ' open from .tme')
        if self.final_status == self.door_open:
            self.tme = int(self.tme)
            self.tme+=self.time_increment
        else:
            self.tme = 0
            self.time_collective = '0'
            save_file('.tme_accum',self.time_collective,'home')
            print(str(self.time_collective) + ' saving to .tme_accum')
        save_file('.tme',str(self.tme),'home')
        print(str(self.tme) + ' saving to .tme')

    def logic(self):

        if self.tme >= self.time_limit:
            self.time_collective = open_file('.tme_accum', 'home')
            print(str(self.time_collective) + ' open from .tme_accum')
            self.time_collective = int(self.time_collective)
            self.time_collective += int(self.tme)
            save_file('.tme_accum', str(self.time_collective), 'home')
            print(str(self.time_collective) + ' saving to .tme_accum')
            self.mail()
            self.tme = 0
            save_file('.tme', str(self.tme), 'home')

            print('Sending text')
        else:
            pass

    def login_info(self):
        ps = open_json('.cred.json', 'home')
        for key, value in ps.items():
            us = key
            psw = value
            return [us,psw]

    def mail(self):
        us, psw = self.login_info()
        print(us)
        print(psw)
        recipients = open_file('.send', 'home').splitlines()
        content = '\n' + 'Garage: ' + self.final_status + \
            ' (' + str(self.time_collective) + ' min notifier)'

        mail = smtplib.SMTP('smtp.gmail.com', 587)

        mail.ehlo()
        mail.starttls()
        mail.ehlo()
        mail.login(us, psw)
        mail.sendmail(us, recipients, content)
        mail.close()


if __name__ == "__main__":
    try:
        while True:
            app = SendMail()
            sleep(refresh)
    except KeyboardInterrupt as e:
        print(e)
        print('Interrupted')
