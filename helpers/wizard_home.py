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

    print(
      f'\n{c.YELLOW}{c.BOLD}We could not find any ' 
      f'configuration{c.END}'
      f'\n{c.GREEN}This Wizard will ask some questions ' 
      f'to setup the configuration needed for the script to function.{c.END}'
      f'\n{c.GREEN}{c.BOLD}This configuration wizard will only run once.{c.END}\n'
      f'\n{c.GREEN}The first 2 questions are going ' 
      f'to be about your email and password you are using to send email. '
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
    
    ipadd = inp.input_single(
      in_message="Enter the IP address for the brooker",
      in_type = "ip"
      )
    
    zip_code = inp.input_single(
      in_message="Enter the US Zip code for weather data",
      in_type = "zip"
      )

    units = inp.input_choice(
    in_message ='Choose the weather unit of measure', 
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
      f'\nThe configuration file has been written to disk'
      f'\nIf you want to change the settings you can edit ' 
      f'{c.CYAN}{c.BOLD}{home}/{conf_dir}/{conf_file}{c.END}'
      f'\n{c.GREEN}{c.BOLD}This wizard ' 
      f'won\'t run any more, So the script can ' 
      f'now be run automatically{c.END}\n'
      f'\n{c.CYAN}{c.BOLD}You can stop ' 
      f'the script by typing Ctrl + C{c.END}\n')

if __name__ == "__main__":
  app = WizardHome()