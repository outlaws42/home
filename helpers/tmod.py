#! /usr/bin/env python3

# -*- coding: utf-8 -*-
version = '2021-05-09'

# Imports included with python
import random
import os
import os.path
import sys
# from smtplib import SMTP
from datetime import datetime, date
from collections import ChainMap # Requires python 3.3
from re import search
import json

from helpers.file import Location as loc
from helpers.colors import Colors as c

# Imports installed through pip
try:
  # pip install pyyaml if needed
  import yaml
except:
  pass

try:
  # pip install cryptography if needed
  from cryptography.fernet import Fernet
except:
  pass

try:
  # pip install requests if needed
  import requests
except:
  pass

try:
  # pip install beautifulsoup4 if needed
  from bs4 import BeautifulSoup  
except:
  pass

# File I/O /////////////////////////////////////////

# def open_file(
#     fname: str,
#     fdest: str = 'relative', 
#     def_content: str = '0',
#     mode: str = 'r'
#     ):
#     """
#     fname = filename, fdest = file destination, 
#     def_content = default value if the file doesn't exist,
#     mode = defines read mode 'r' or 'rb'
#     Opens the file if it exists and returns the contents.
#     If it doesn't exitst it creates it. Writes 
#     the def_content value to it and returns the def_content value
#     import os
#     """
#     home = loc.home_dir()
#     try:
#         if fdest == 'home' or fdest == 'Home':
#             with open(f'{home}/{fname}', mode) as path_text:
#                 content=path_text.read()
#         else:
#             with open(loc.get_resource_path(fname), mode) as text:
#                 content=text.read()
#         return content
#     except(FileNotFoundError) as e:
#         print(e)
#         print('It is reading here')
#         if fdest == 'home' or fdest == 'Home':
#             with open(f'{home}/{fname}', 'w') as output:
#                 output.write(def_content)
#         else:
#             with open(loc.get_resource_path(fname), 'w') as output:
#                 output.write(def_content)
#         return def_content

# def save_file(
#     fname: str,
#     content: str,
#     fdest: str ='relative', 
#     mode: str = 'w'):
#     """
#     fname = filename, content = what to save to the file, 
#     fdest = where to save file, mode = w for write or a for append
#     import os
#     """
#     home = loc.home_dir()
#     if fdest == 'home' or fdest == 'Home':
#         with open(f'{home}/{fname}', mode) as output:
#             output.write(content)
#     else:
#         with open(loc.get_resource_path(fname), mode) as output:
#             output.write(content)
# def save_file_append(file_,variable,type_='relative'):
#     home = os.path.expanduser("~")
#     if type_ == 'home' or type_ == 'Home':
#         with open(f'{home}/{file_}', 'a') as output:
#             output.write(variable)
#     else:
#         with open(loc.get_resource_path(file_), 'a') as output:
#             output.write(variable)

# def save_json(file_,variable,type_='relative'):
#     home = os.path.expanduser("~")
#     if type_ == 'home' or type_ == 'Home':
#         with open(f'{home}/{file_}', 'w') as output:
#             json.dump(variable,output, sort_keys=True, indent=4)
#     else:
#         with open(loc.get_resource_path(file_), 'w') as output:
#             json.dump(variable,output, sort_keys=True, indent=4)
                
# def open_json(file_,type_='relative'):
#     home = os.path.expanduser("~")
#     try:
#         if type_ == 'home' or type_ == 'Home':
#             with open(f'{home}/{file_}', 'r') as fle:
#                     variable = json.load(fle)
#             return variable
#         else:
#             with open(loc.get_resource_path(file_), 'r') as fle:
#                     variable = json.load(fle)
#             return variable
#     except(FileNotFoundError, EOFError) as e:
#         print(e)
#         variable = 0
#         if type_ == 'home' or type_ == 'Home':
#             with open(f'{home}/{file_}', 'w') as fle:
#                 json.dump(variable, fle)
#         else:
#             with open(loc.get_resource_path(file_), 'w') as fle:
#                 json.dump(variable, fle)

# def save_yaml(
#     fname: str,
#     content: dict,
#     fdest: str ='relative',
#     mode: str = 'w'
#     ):
#     """
#     fname = filename, content = data to save, fdest = file destination,
#     mode = 'w' for overwrite file or 'a' to append to the file
#     Takes a dictionary and writes it to file specified. it will either
#     write or append to the file depending on the mode method
#     requires: import os, yaml
#     """
#     home = loc.home_dir()
#     if fdest == 'home' or fdest == 'Home':
#         with open(f'{home}/{fname}', mode) as output:
#             yaml.safe_dump(content,output, sort_keys=True)
#     else:
#         with open(loc.get_resource_path(fname), mode) as output:
#             yaml.safe_dump(content,output, sort_keys=True)

# def open_yaml(
#     fname: str,
#     fdest: str ='relative',
#     def_content: dict = {'key': 'value'}
#     ):
#     """
#     fname = filename, fdest = file destination, 
#     def_content = default value if the file doesn't exist
#     opens the file if it exists and returns the contents
#     if it doesn't exitst it creates it writes 
#     the def_content value to it and returns the def_content value
#     import os, yaml(pip install pyyaml)
#     """
#     home = loc.home_dir()
#     try:
#         if fdest == 'home' or fdest == 'Home':
#             with open(f'{home}/{fname}', 'r') as fle:
#                     content = yaml.safe_load(fle)
#             return content
#         else:
#             with open(loc.get_resource_path(fname), 'r') as fle:
#                     content = yaml.safe_load(fle)
#             return content
#     except(FileNotFoundError, EOFError) as e:
#         print(e)
#         if fdest == 'home' or fdest == 'Home':
#             with open(f'{home}/{fname}', 'w') as output:
#                 yaml.safe_dump(def_content,output, sort_keys=True)
#         else:
#             with open(loc.get_resource_path(fname), 'w') as output:
#                 yaml.safe_dump(def_content,output, sort_keys=True)
#         return def_content
  
              
# def open_log_file(file_,type_='home'):
#     home = os.path.expanduser("~")
#     try:
#         if type_ == 'home' or type_ == 'Home':
#             with open(f'{home}/Logs/{file_}', 'r') as path_text:
#                 variable=path_text.read()
#         else:
#             with open(loc.get_resource_path(file_), 'r') as text:
#                 variable=text.read()
#         return variable
#     except(FileNotFoundError) as e:
#         print(e)
#         print('It is reading here')
#         variable = '0'
#         if type_ == 'home' or type_ == 'Home':
#             with open(f'{home}/{file_}', 'w') as output:
#                 output.write(variable)
#         else:
#             with open(loc.get_resource_path(file_), 'w') as output:
#                 output.write(variable)

# def check_dir(
#   dname: str, 
#   ddest: str = 'home'
#   ):
#   """
#   dname = name of the file or folder,
#   ddest = the destination, either home or relative to CWD
#   check to see if specified dir exists.
#   Requires import os
#   """
#   home = loc.home_dir()
#   if ddest == 'home' or ddest == 'Home':
#     dpath = f'{home}/{dname}'
#   else:
#     dpath = loc.get_resource_path(dname)
#   dir_exist = os.path.isdir(dpath)
#   return dir_exist

# def make_dir(
#   dname:str, 
#   ddest: str = 'home'
#   ):
#   """
#   dname = name of the file or folder,
#   ddest = the destination, either home or relative to CWD
#   Makes the dir specified.
#   Requires import os
#   """
#   home = loc.home_dir()
#   if ddest == 'home' or ddest == 'Home':
#     os.mkdir(f'{home}/{dname}')
#   else:
#     os.mkdir(loc.get_resource_path(dname))


# def remove_file(
#   fname:str, 
#   fdest: str = 'home'
#   ):
#   """
#   fname = name of the file or folder,
#   fdest = the destination, either home or relative to CWD
#   Removes the file specified
#   Requires import os
#   """
#   home = loc.home_dir()
#   if fdest == 'home' or fdest == 'Home':
#     os.remove(f'{home}/{fname}')
#   else:
#     os.remove(loc.get_resource_path(fname))

# def check_file_dir(
#   fname: str, 
#   fdest: str = 'home'
#   ):
#   """
#   fname = name of the file or folder,
#   fdest = the destination, either home or relative to CWD
#   Check if file or folder exist returns True or False
#   Requires import os
#   """
#   home = loc.home_dir()
#   if fdest == 'home' or fdest == 'Home':
#     fpath = f'{home}/{fname}'
#   else:
#     fpath = loc.get_resource_path(fname)
#   file_exist = os.path.exists(fpath)
#   return file_exist

# Encryption

# def gen_key(fname: str,):
#   home = loc.home_dir()
#   key = Fernet.generate_key()
#   with open(f'{home}/{fname}', 'wb')as fkey:
#     fkey.write(key)

# def encrypt(
#   key: str, 
#   fname: str, 
#   e_fname: str, 
#   fdest='relative', 
#   ):
#   """
#   key = key file used to encrypt file,
#   fname = file to encrypt,
#   e_fname = name of the encrypted file,
#   fdest = file destination relative too,
#   Takes a input file and encrypts output file
#   requires tmod open_file and save_file functions
#   requires from cryptography.fernet import Fernet
#   """
#   keyf = Fernet(key)
#   e_file = open_file(
#     fname = fname,
#     fdest = fdest,
#     mode = "rb"
#     )
#   encrypted_file = keyf.encrypt(e_file)
#   save_file(
#     fname = e_fname,
#     content = encrypted_file,
#     fdest = fdest,
#     mode = "wb"
#   )

# def decrypt_login(
#   key: str, 
#   e_fname: str,
#   fdest: str = 'relative'
#   ):
#   keyf = Fernet(key)
#   encrypted = open_file(
#     fname = e_fname,
#     fdest = fdest,
#     mode = "rb"
#     )
#   decrypt_file = keyf.decrypt(encrypted)
#   usr = decrypt_file.decode().split(':')
#   return [usr[0],usr[1]]

# Gleen info ////////////////////////////////////////////////////
def html_info(tag,url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        find_status = soup.find(tag)
        final_status = find_status.text.strip()
    except requests.exceptions.RequestException as e:
        print(e)
        final_status = "Can't connect"
        print(final_status)
    return final_status

def list_of_items(item,range_num: int):
        """
        item = the data you want added
        range_num = how many items to add
        Add items to a list in 
        the range of range_numb
        """    
        items_list = []
        for i in range(range_num):
            temp = item
            items_list.append(temp)
        return items_list

# def add_to_list(list_in,list_out):
#     # takes a list of items
#   for i in range(len(list_in)):
#     list_out.append(list_in[i])
#   return list_out

# def dict_to_list(dictionary: dict):
#   """
#    Convert dictionary to a list
#   """
#   temp = []
#   list_name = []
#   for key, value in dictionary.items():
#     temp = [key,value]
#     list_name.append(temp)
#   return list_name.sort()

# def combine_dict(dict_list):
#         """
#         Takes a list of dictionarys and combines into one dictionary
#         requires from collections import ChainMap and python 3.3 or later
#         """
#         current = dict(ChainMap(*dict_list))
#         return current

def group_list(list_, positions, start=0):
    """
    takes a list and groups them into sub list in the amount of positions
    """
    while start <= len(list_) - positions:
        yield list_[start:start + positions]
        start += positions

def random_list(list_):
    """
        Randomizes a list
    """
    for item in range(1):
        rand = random.sample(list_, len(list_))
    return rand

def reverse_sublist(self,list_):
    for i in range(0,len(list_),2):
        list_[i][:] = list_[i][::-1]
    return list_
    
def last_n_lines(fname, lines, fdest='relative'):
  """
  Gets the last so many lines of a file 
  and returns those lines in text.
  Arguments = filename, number of lines
  """
  home = os.path.expanduser("~")
  try:
    file_lines = []
    if fdest == 'home' or fdest == 'Home':
      with open(f'{home}/{fname}') as file:
        for line in (file.readlines() [-lines:]):
          file_lines.append(line)
    else:
      with open(loc.get_resource_path(fname), 'r') as file:
        for line in (file.readlines() [-lines:]):
          file_lines.append(line)
    file_lines_text = (''.join(file_lines))
    return file_lines_text
  except(FileNotFoundError) as e:
    print(e)
    return 'file not found'

# Date/Time//////////////////////////////////////////////
def day_diff(month,day,year):
    current = date.today()
    day = date(year,month,day)
    till_day = day - current
    return till_day.days
    
def year_current():
    current = date.today()
    current_year = current.year
    return current_year
    
def time_now():
    current =  datetime.now().strftime('%H:%M:%S')
    return current

def timestamp_from_string_time(str_time):
    '''
    Takes a string time with AM or PM and 
    converts it to a Unix timestamp
    '''
    dt_time = datetime.strptime(str_time, '%I:%M %p').time()
    today_date = datetime.today().date()
    str_date = today_date.strftime('%Y-%m-%d')
    year, month, day = str_date.split('-')
    dt = datetime.combine(
      date(int(year), int(month), int(day)), dt_time)
    ts = int(dt.timestamp())
    return ts



def import_temp(file_='temp.txt'):
    '''
    Import temp from text file then split off each word. 
    returns current temp  
    '''
    tempin = open_file(file_)
    templist = tempin.split()
    temp, day, hour = templist
    now_hour = datetime.datetime.now().strftime('%H.%M')
    temp_diff = round(float(now_hour) - float(hour))
        
    if temp_diff == 0:  
        if temp > '0':
            print(f'Temp diff: {temp_diff}')
            print(f'This is the temp: {temp}')
            current_temp = temp
        else:
                current_temp = 'Bad Reading'
    else:
        current_temp = 'Sensor Needs Reset'
        print('Sensor needs reset')
        
    return current_temp
        
def try_float(temp):
    '''
    Try's to change a string into a float. 
    if it fails it returns original temp
    if it converts it returns the temp as a float
    '''
    try:
        temp = float(temp)
    except Exception as e:
        print(e)
        temp = temp
    return temp

    
# file information



# Send/Receive

# def mail(
#   body: str, 
#   subject: str,
#   send_to: list,
#   login: list
#   ):
#   """
#   body = Body of the message, subject = The subject,
#   send_to = Who you want to send the message to,
#   login = The login information for email.
#   Requires from smtplib import SMTP
#   """
#   us, psw = login
#   message = f'Subject: {subject}\n\n{body}'
#   print(message)
#   try:
#     mail = SMTP('smtp.gmail.com', 587)
#     mail.ehlo()
#     mail.starttls()
#     mail.ehlo()
#     mail.login(us, psw)
#     mail.sendmail(us,send_to, message)
#     mail.close()
#     print('Successfully sent email')
#   except Exception as e:
#     print('Could not send email because')
#     print(e)


## Wizard setup
# def config_setup(conf_dir: str):
#   """
#   conf_dir = Configuration dir. This would 
#   normally be in the .config/progName,
#   This commandline wizard creates the 
#   program config dir and populates the 
#   setup configuration file. Sets up username 
#   and password for email notifications
#   """
#   c = colors()
#   home = loc.home_dir()
#   make_dir(conf_dir)

#   print(
#     f'\n{c["YELLOW"]}{c["BOLD"]}We could not find any ' 
#     f'configuration folder{c["END"]}'
#     f'\n{c["GREEN"]}This Wizard will ask some questions ' 
#     f'to setup the configuration needed for the script to function.{c["END"]}'
#     f'\n{c["GREEN"]}{c["BOLD"]}This configuration wizard will only run once.{c["END"]}\n'
#     f'\n{c["GREEN"]}The first 2 questions are going ' 
#     f'to be about your email and password you are using to send. '
#     f'\nThis login information will be stored on your local ' 
#     f'computer encrypted seperate '
#     f'\nfrom the rest of the configuration. ' 
#     f'This is not viewable by browsing the filesystem{c["END"]}'
#   )

#   gen_key(f'{conf_dir}/.info.key')
#   key = open_file(
#       fname = f'{conf_dir}/.info.key', 
#       fdest = "home",
#       mode ="rb"
#       )

#   email = input_single(
#     in_message = "\nEnter your email",
#     in_type = 'email'
#    )
#   pas = input_single(
#     in_message = "\nEnter your password",
#     in_type = 'password')
#   lo = {email:pas}
#   save_yaml(
#     fname = f'{conf_dir}/.cred.yaml',
#     fdest = 'home',
#     content = lo
#     )
#   encrypt(
#     key = key,
#     fname = f'{conf_dir}/.cred.yaml',
#     e_fname = f'{conf_dir}/.cred_en.yaml',
#     fdest = 'home'
#     )
#   remove_file(f'{conf_dir}/.cred.yaml')
#   run = input_single(
#     in_message ="Enter the time to run the script daily(Example: 05:00)",
#     in_type = "time"
#     )
#   numb_lines = input_single(
#     in_message='Enter the number of lines from the end of log file to send',
#     in_type = 'int',
#     max_number = 400
#     )
#   send_list = input_list(
#     subject= "email address",
#     description = 'to send to (example@gmail.com)',
#     in_type = 'email')
#   log_list = input_list(
#     subject= "log file",
#     description = 'to check relative to your home dir (Example: Logs/net_backup.log)',
#     in_type = 'file'
#     )
#   load = {
#     'runtime': run,
#     'lines': int(numb_lines),
#     'sendto': send_list,
#     'logs': log_list
#     }
#   save_yaml(
#     fname =f'{conf_dir}/emailog_set.yaml',
#     fdest = 'home',
#     content = load)
#   print(
#     f'\n{c["YELLOW"]}{c["BOLD"]}This completes the wizard{c["END"]}'
#     f'\nThe configuration file has been written to disk'
#     f'\nIf you want to change the settings you can edit ' 
#     f'{c["CYAN"]}{c["BOLD"]}{home}/{conf_dir}/emailog_set.yaml{c["END"]}'
#     f'\n{c["GREEN"]}{c["BOLD"]}This wizard ' 
#     f'won\'t run any more, So the script can ' 
#     f'now be run automatically{c["END"]}\n'
#     f'\n{c["CYAN"]}{c["BOLD"]}You can stop ' 
#     f'the script by typing Ctrl + C{c["END"]}\n')