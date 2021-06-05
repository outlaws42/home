from re import T, search
from datetime import datetime
from helpers.colors import Colors as c
from helpers.file import FileInfo
from helpers.validate_input import ValidateInput

fi = FileInfo()
vi = ValidateInput()

class Inp():
  
  def input_list(
    self,
    subject: str, 
    description: str,
    in_type: str = 'email',
    outword: str = 'next'
    ):
    """
    subject = The subject of the input item,\n
    description = the description of the input item,\n
    in_type = the type of input field. Choices are\n 
      'email' - This will expect a email address\n 
      'file' - this will expect a valid file at location specified\n 
      'number' - This will expect a number\n 
      'time12' - this will expect a 12 hour time (HH:MM am or pm)\n 
      'time24' - This will expect a 24 hour time (HH:MM)\n
      'password' - This will expect a password\n
      'ip4' - This will expect a ipv4 ip\n 
      'ip6' - This will expect a ipv6 ip\n 
      'zip5' - This will expect a 5 digit US zip code\n 
      'zip9' - This will expect a 9 digit US zip code\n
    outward = This is the word used to present to the user
    to stop adding more items.
    This would be used for a input item that you would
    want to add to a list.
    """
    print(
      f'\n{c.PURPLE}{c.BOLD}'
      f'{subject.capitalize()}{c.END}\n'
      f'{c.BOLD}You can add as many items as you like.\n'
      f'But you must add at least 1 item.\n'
      f'When your done adding, Type ' 
      f'{c.RED}{outword}{c.END}\n'
    )
    item_list = []
    while True:
      item: str = input(
          f"{c.BOLD}Enter the {subject} {description}:{c.END} ")
      print("\n")
      while (self.validate_input(item, in_type) == False):
        if ((
          item == outword or 
          item == outword.capitalize() or 
          item == outword.upper()) and 
          len(item_list) != 0
        ):
          break
        if item == outword or item == outword.capitalize() or item == outword.upper():
          print(
            f'{c.RED}{c.BOLD}You need to enter at least 1 ' 
            f'{in_type}{c.END}')
        else:
          print(
            f'{c.RED}{c.BOLD}This is not a valid ' 
            f'{in_type}{c.END}')
        item: str = input(
          f"{c.BOLD}Enter the {subject} {description}:{c.END} ")
        # print('\n')
      if ((
        item == outword or 
        item == outword.capitalize() or 
        item == outword.upper()) and
        len(item_list) != 0
        ):
        length = len(item_list)
        print(
          f'{c.BOLD}You have added {length} item(s), ' 
          f'Because you typed {c.RED}{item}{c.END}\n'
          f'{c.BOLD}That will complete your selection for ' 
          f'"{subject.capitalize()}".{c.END}\n')
        break
      else:
        print(f'{c.BOLD}You added {c.CYAN}{item}{c.END}\n')
        print(f"{c.BOLD}Total List{c.END}")
        item_list.append(item)
        for i in item_list:
          print(f'{c.BOLD}{c.CYAN}{i}{c.END}')
    # print('\n')
    return item_list
  
  def input_password(
    self, 
    lower: str = '1',
    upper: str = '1',
    number: str = '1',
    special: str = '1',
    length: str = '8'
    ):
    """
    upper = Minimum uppercase characters required\n
    lower = Minimum lowercase characters required\n
    number = Minimum numbers required\n
    special = Minimum special characters required\n
    length = Minimum characters the password needs to be\n
    """
    print(
      f'\n{c.BOLD}{c.PURPLE}Password Minumum Requirements\n'
      f'{c.GREEN}{lower}{c.WHITE} lowercase character(s),\n'
      f'{c.GREEN}{special}{c.WHITE} of * # $ % & !,\n' 
      f'{c.GREEN}{upper}{c.WHITE} UPPERCASE character(s),\n'
      f'{c.GREEN}{number}{c.WHITE} number\n' 
      f'{c.GREEN}{length}{c.WHITE} characters long{c.END}')
    item = input(f'{c.BOLD}{c.YELLOW}Enter a password: {c.END}')
    while(vi.validate_password(
      item=item,
      lower=lower,
      upper=upper,
      number=number,
      special=special,
      length=length)==False):
      print(f'\n{c.BOLD}{c.RED}This is not valed, you entered {c.WHITE}{item}\n'
      f' It doesn\'t meet the minimum requirements{c.END}')
      item = input(f'{c.BOLD}{c.YELLOW}Enter a password: {c.END}')
    print(f'\n{c.BOLD}That is a valid password {c.END}')
    return item

  def input_single(
    self,
    in_message: str,
    in_type: str ='email',
    fdest: str = 'home',
    max_number: int = 200,
    default = '',
    req: str = None
    ):
    """
    in_message = the message you want in your input string,\n
    in_type = the type of input field. Choices are\n 
      'email' - This will expect a email address\n 
      'file' - this will expect a valid file at location specified\n 
      'number' - This will expect a number\n 
      'time12' - this will expect a 12 hour time (HH:MM am or pm)\n 
      'time24' - This will expect a 24 hour time (HH:MM)\n
      'ip4' - This will expect a ipv4 ip\n 
      'ip6' - This will expect a ipv6 ip\n 
      'zip5' - This will expect a 5 digit US zip code\n 
      'zip9' - This will expect a 9 digit US zip code\n
    max_number = if a number input the max number you can enter
    This is for a single item input. This uses "validate_input"
    to verify that items entered meet requirements for that type of input
    """
    if in_type == 'int' or in_type == 'float':
      item = input(
          f'{c.BOLD}{in_message}{c.GREEN}(max {max_number}) ' 
          f'(Default: {default}): {c.END}') or default
    else:
      item = input(
        f'{c.BOLD}{in_message} {c.GREEN}(Default: '
        f'{default}): {c.END}') or default
    while (self.validate_input(
      item = item, 
      in_type = in_type,
      fdest = fdest,
      max_number = max_number
      ) == False):
      print(
        f'{c.RED}{c.BOLD}'
        f'This is not a valid {in_type}{c.END}\n')
      if in_type == 'int' or in_type == 'float':
        item = input(
          f'{c.BOLD}{in_message}{c.GREEN}(max {max_number}) ' 
          f'(Default: {default}): {c.END}') or default
      else:
        item = input(
        f'{c.BOLD}{in_message} {c.GREEN}(Default: '
        f'{default}): {c.END}') or default
    
    print(f'\n{c.BOLD}You entered {c.CYAN}{item}{c.END}\n')
    if in_type == 'int':
      return int(item)
    elif in_type == 'float':
      return float(item)
    else:
      return item
  
  def input_choice(
    self,
    in_message: str,
    choices: dict = {1: 'option 1', 2: 'option 2'}, 
    default_choice: int = 1
    ):
    """
    in_message = the message you want in your input string,\n
    choices = dictionary of options for your choices.
    The key being a int the user will select. The value
    being the option used\n
    default_choice = This is the choice that will be
    selected if the user doesn't choose any option. 

    """
    
    print(f"\n{c.BLUE}{c.BOLD}Select a item from the following items{c.END}" )
    for key, value in choices.items():
      print(f"{c.BOLD}{key} = {c.YELLOW}{value}{c.END}")
    try:
      item = input(
       f'{c.BOLD}{in_message} {c.GREEN}(default {default_choice}):{c.END} ') or default_choice
      item = int(item)
    except ValueError:
      print('select a valid option')
      item = 1000
    while (item not in choices.keys()):
      try:
        item = input(
       f'{c.BOLD}{in_message} {c.GREEN}(default {default_choice}):{c.END} ') or default_choice
        item = int(item)
      except ValueError:
        print('Select a valid option')
        item = 1000
    choice = choices[item]
    print(
      f'{c.BOLD}You chose {c.YELLOW}{choice}{c.END}')
    return choice

  def validate_input(
    self,
    item: str,
    in_type: str,
    fdest: str = 'home',
    max_number: int = 200 
    ):
    """
    item = The data entered in the input field,
    in_type = The type of data it is suposed to be,
    email address\n
    ip address = 'ip4' or 'ip6'\n

    max_number = the max number that can be applied this is for int only.
    Takes the input and checks to see if it is 
    valid for its data type.
    """
    if in_type == 'email':
      vi.validate_email(item=item)
    elif in_type == 'ip4' or in_type == 'ip6':
     vi.validate_ip(item=item, ip_type=in_type)
    elif in_type == 'zip5' or in_type == 'zip9':
      vi.validate_zip(item=item, zip_type=in_type)
    elif in_type == 'file':
     vi.validate_file(item=item,fdest=fdest)
    elif in_type == 'password':
     vi.validate_password(item=item)
    elif in_type == 'time24' or in_type == 'time12':
      vi.validate_time(item=item, time_type=in_type)
    elif in_type == 'number':
      vi.validate_num(item=item, max_number=max_number)
    else:
      return False

if __name__ == "__main__":
  app = Inp()
  test = app.input_choice(
    in_message ='Choose the weather unit of measure', 
    choices = {
      1: 'imperial', 
      2: 'metric',
    } )
  