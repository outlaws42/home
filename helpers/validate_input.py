from re import search
from datetime import datetime
from helpers.file import FileInfo

fi = FileInfo()

class ValidateInput():

  def validate_email(
    self,
    item: str,
    ):
    """
    item = email address,\n
    checkes the entered email to the sequence\n
    returns True or False depending if it is a valid email
    """
    val_email = (
      r'^[a-zA-Z0-9]+([#$&_*?^{}~-][a-zA_Z0-9]+)*'
      r'(\.[a-zA-Z0-9#$&_*?^{}~-]+)*[@]\w+[_.-]?\w+[.]\w{2,3}$')
    if (search(val_email,item)):
      return True
    else:
      return False

  def validate_ip(
    self, 
    item: str,
    ip_type: str = 'ip4'
    ):
    """
    item = ipv4 or ipv6 ip address ,\n
    ip_type = 'ip4', 'ip6' what type of ip to compare,\n
    return True or False depending if it matches the sequence\n
    according to type.
    """
    if ip_type == 'ip4':
      val_ip =(
      r'^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}'
      r'(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$')
    elif ip_type == 'ip6':
      pass
    else:
      return False
    if (search(val_ip,item)):
      return True
    else:
      return False

  def validate_zip(
    self, 
    item: str, 
    zip_type: str = 'zip5'
    ):
    """
    item = 5 or 9 digit zip,\n
    zip_type = 'zip5', 'zip9' what type of zip code to compare,\n
    return True or False depending if it matches the sequence\n
    according to type.
    """
    if zip_type == 'zip5':
      val_zip = "^\d{5}$"
    elif zip_type == 'zip9':
      val_zip = "^([0-9]{5})(-[0-9]{4})?$"
    else:
      return False
    if (search(val_zip,item)):
      return True
    else:
      return False
   
  def validate_file(
    self, 
    item: str,
    fdest: str = 'home'
    ):
    if not item:
      return False
    else:
      return fi.check_file_dir(item, fdest)
    
  def validate_password(
    self, 
    item: str,
    upper: str = '1',
    lower: str = '1',
    number: str = '1',
    special: str = '1',
    length: str = '8',
    ):
    """
    item = password\n
    upper = Minimum uppercase characters required\n
    lower = Minimum lowercase characters required\n
    number = Minimum numbers required\n
    special = Minimum special characters required\n
    length = Minimum characters the password needs to be\n
    return True if item meets the requirements\n
    """
    val_pass = (
      r'^(?=(?:.*[a-z]){'+lower+'})(?=(?:.*[A-Z]){'+upper+'})'
      r'(?=(?:.*[0-9]){'+number+'})(?=(?:.*[*#$%&!]){'+special+'})'
      r'[A-Za-z0-9*#$%&!]{'+length+',}$')
    if not item:
      return False
    if (search(val_pass,item)):
      return True
    else:
      return False
  
  def validate_time(
    self, 
    item: str,
    time_type: str = 'time24'
    ):
    """
    item = 24 (HH:MM) or 12 (HH:MM AM or PM) hour time,\n
    time_type = '24', '12' what type of time to compare,\n
    return True or False depending if it matches the datetime\n
    format according to type.
    """
    try:
      if time_type == 'time24':
        datetime.strptime(item,'%H:%M').time()
      elif time_type == 'time12':
        datetime.strptime(item,'%I:%M %p').time()
      else:
        return False
      return True
    except ValueError:
      return False

  def validate_num(
    self, 
    item: str, 
    max_number: float= 200.0
     ):
     """
    item = number,\n
    return True or False depending if it matches the sequence\n
    and doesn't exceed the max number specified.
    """
     val_num = '^[0-9]+(,[0-9]+)*(\.[0-5]+)?$'
     if (search(val_num,item)):
       if float(item) <= max_number:
         return True
       else:
         return False
     else:
       return False
