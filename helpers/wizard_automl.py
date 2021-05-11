from helpers.colors import Colors as c
from helpers.file import (
  Location as loc, FileInfo as fi, FileEdit as fe
  )
from helpers.io import IO as io
from helpers.inp import Inp as inp
from helpers.encrypt import Encryption as en

def open_settings(conf_dir, conf_file):
  settings = io.open_yaml(
    fname = f"{conf_dir}/{conf_file}", 
    fdest = "home"
    )
  print(settings)
  return settings['SENDTO']

def automl_config_exist(conf_dir: str, conf_file: str):
   file_exists = fi.check_file_dir(
     fname = f'{conf_dir}/{conf_file}', 
     fdest = 'home'
     )
   if file_exists == False:
     config_setup(conf_dir, conf_file)
   elif file_exists == True:
     try:
       open_settings(conf_dir, conf_file)
       return True
     except Exception as e:
       print(e)
       print(f'File doesn\'t exists or has no SENDTO')
       return False

def file_set(
  send_list: list,
  conf_dir: str,
  conf_file: str
  ):
  file_exists = fi.check_file_dir(f'{conf_dir}/{conf_file}')
  if file_exists == False:
    load = {
      'USE_API': True,
      'API': 2,
      'BROKER_ADDRESS': '192.168.1.3',
      'ZIP_CODE': '46764',
      'UNITS': 'imperial',
      'DB_URI': 'mongodb://localhost:27017',
      'DATABASE': 'home',
      'SENDTO': send_list,
      }
  else:
    loaded = io.open_yaml(
      fname = f'{conf_dir}/{conf_file}',
      fdest = 'home'
      )
    load = {
      'USE_API': loaded['USE_API'],
      'API': loaded['API'],
      'BROKER_ADDRESS': loaded['BROKER_ADDRESS'],
      'ZIP_CODE': loaded['ZIP_CODE'],
      'UNITS': loaded['UNITS'],
      'DB_URI': loaded['DB_URI'],
      'DATABASE': loaded['DATABASE'],
      'SENDTO': send_list,
      }
  return load


def config_setup(conf_dir: str, conf_file: str):
  """
  conf_dir = Configuration dir. This would 
  normally be in the .config/progName,
  This commandline wizard creates the 
  program config dir and populates the 
  setup configuration file. Sets up username 
  and password for email notifications
  """
  # c = colors()
  home = loc.home_dir()
  dir_exists = fi.check_dir(conf_dir)

  if dir_exists == False:
    fe.make_dir(conf_dir)

  # file_exists = check_file_dir(f'{conf_dir}/{conf_file}')

  print(
    f'\n{c.YELLOW}{c.BOLD}We could not find any ' 
    f'configuration folder{c.END}'
    f'\n{c.GREEN}This Wizard will ask some questions ' 
    f'to setup the configuration needed for the script to function.{c.END}'
    f'\n{c.GREEN}{c.BOLD}This configuration wizard will only run once.{c.END}\n'
    f'\n{c.GREEN}The first 2 questions are going ' 
    f'to be about your email and password you are using to send. '
    f'\nThis login information will be stored on your local ' 
    f'computer encrypted seperate '
    f'\nfrom the rest of the configuration. ' 
    f'This is not viewable by browsing the filesystem{c.END}'
  )
  # sento_exists = automl_config_exist(conf_dir, conf_file)

  kf_exists = fi.check_file_dir(f'{conf_dir}/info.key')
  cred_exists = fi.check_file_dir(f'{conf_dir}/.cred_en.yaml')

  if kf_exists == False and cred_exists == False:
    en.gen_key(f'{conf_dir}/.info.key')
    key = io.open_file(
        fname = f'{conf_dir}/.info.key', 
        fdest = "home",
        mode ="rb"
        )

    email = inp.input_single(
      in_message = "\nEnter your email",
      in_type = 'email'
    )
    pas = inp.input_single(
      in_message = "\nEnter your password",
      in_type = 'password')
    lo = {email:pas}
    io.save_yaml(
      fname = f'{conf_dir}/.cred.yaml',
      fdest = 'home',
      content = lo
      )
    en.encrypt(
      key = key,
      fname = f'{conf_dir}/.cred.yaml',
      e_fname = f'{conf_dir}/.cred_en.yaml',
      fdest = 'home'
      )
    fe.remove_file(f'{conf_dir}/.cred.yaml')
  else:
    print('cred already exists')

  send_list = inp.input_list(
    subject= "email address",
    description = 'to send to (example@gmail.com)',
    in_type = 'email')
  
  content = file_set(
    send_list = send_list,
    conf_dir = conf_dir,
    conf_file = conf_file
    )
  io.save_yaml(
    fname =f'{conf_dir}/{conf_file}',
    fdest = 'home',
    content = content)
  print(
    f'\n{c.YELLOW}{c.BOLD}This completes the wizard{c.END}'
    f'\nThe configuration file has been written to disk'
    f'\nIf you want to change the settings you can edit ' 
    f'{c.CYAN}{c.BOLD}{home}/{conf_dir}/{conf_file}{c.END}'
    f'\n{c.GREEN}{c.BOLD}This wizard ' 
    f'won\'t run any more, So the script can ' 
    f'now be run automatically{c.END}\n'
    f'\n{c.CYAN}{c.BOLD}You can stop ' 
    f'the script by typing Ctrl + C{c.END}\n')