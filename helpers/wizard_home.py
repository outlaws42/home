from sys import platform
from helpers.colors import Colors as c
from helpers.file import (
  Location, FileInfo, FileEdit
  )
from helpers.io import IO
from helpers.inp import Inp
from helpers.encrypt import Encryption

loc = Location()
fi  = FileInfo()
fe = FileEdit()
io = IO()
inp = Inp()
en = Encryption()

def get_ip():
  # os = platform
  if platform.startswith('linux'): 
    ipaddr = fi.command_var("hostname -I")
  elif platform.startswith("windows"):
    ipaddr = fi.command_var("ipconfig /release")
  elif platform.startswith("darwin"):
    ipaddr = fi.command_var("ifconfig |grep inet")
  return ipaddr

class WizardHome():

  def __init__(self):
    pass

  def config_setup(self,conf_dir: str, conf_file: str):
    """
    conf_dir = Configuration dir. This would 
    normally be in the .config/progName,
    This commandline wizard creates the 
    program config dir and populates the 
    setup configuration file. Sets up username 
    and password for email notifications
    """
    home = loc.home_dir()
    dir_exists = fi.check_dir(conf_dir)

    if dir_exists == False:
      fe.make_dir(conf_dir)
    kf_exists = fi.check_file_dir(f'{conf_dir}/info.key')
    cred_exists = fi.check_file_dir(f'{conf_dir}/.cred_en.yaml')

    print(
      f'\n{c.YELLOW}{c.BOLD}We could not find any ' 
      f'configuration{c.END}'
      f'\n{c.GREEN}{c.BOLD}This Wizard will ask some questions ' 
      f'to setup the configuration needed for the script to function.'
      f'\nThis configuration wizard will only run once.{c.END}\n'
    )

    if kf_exists == False and cred_exists == False:

      print(
        f'{c.BOLD}{c.GREEN}The first 2 questions are going ' 
        f'to be about your email and password you are using to send email. '
        f'\nThis login information will be stored on your local ' 
        f'computer encrypted seperate '
        f'\nfrom the rest of the configuration. ' 
        f'This is not viewable by browsing the filesystem{c.END}'
      )

      en.gen_key(f'{conf_dir}/.info.key')
      key = io.open_file(
          fname = f'{conf_dir}/.info.key', 
          fdest = "home",
          mode ="rb"
          )

      email = inp.input_single(
        in_message = "\nEnter your email",
        in_type = 'email',
        default = 'appmonitor42@gmail.com'
      )
      pas = inp.input_password()
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
      pass

    send_list = inp.input_list(
      subject= "email address",
      description = 'to send to (example@gmail.com)',
      in_type = 'email')

    ip = get_ip()
    ipadd = inp.input_single(
      in_message="Enter the IP address for the broker",
      in_type = "ip4",
      default = ip
      )
    
    zip_code = inp.input_single(
      in_message="Enter the 5 digit US Zip code for weather data",
      in_type = "zip5"
      )

    units = inp.input_choice(
    in_message ='Choose the unit of measure for weather collection', 
    choices = {
      1: 'imperial', 
      2: 'metric',
    } )

    load = {
        'USE_API': True,
        'API': 2,
        'BROKER_ADDRESS': ipadd,
        'ZIP_CODE': zip_code,
        'UNITS': units,
        'DB_URI': 'mongodb://localhost:27017',
        'DATABASE': 'home',
        'SENDTO': send_list,
        }

    io.save_yaml(
      fname =f'{conf_dir}/{conf_file}',
      fdest = 'home',
      content = load)
    print(
      f'\n{c.YELLOW}{c.BOLD}This completes the wizard{c.END}'
      f'\n{c.BOLD}The configuration file has been written to disk'
      f'\nIf you want to change the settings you can edit ' 
      f'{c.CYAN}{home}/{conf_dir}/{conf_file}{c.END}'
      f'\n{c.GREEN}{c.BOLD}This wizard ' 
      f'won\'t run any more, So the script can ' 
      f'now be run automatically{c.END}\n'
      f'\n{c.CYAN}{c.BOLD}You can stop ' 
      f'the script by typing Ctrl + C{c.END}\n')

if __name__ == "__main__":
  app = WizardHome()