from re import search
from datetime import datetime
from helpers.colors import Colors as c
from helpers.file import FileInfo

fi = FileInfo()

class Inp():
  
  def input_list(
    self,
    subject: str, 
    description: str,
    in_type: str = 'email',
    outword: str = 'next'
    ):
    """
    subject = The subject of the input item,
    description = the description of the input item,
    in_type = tthe type of input field. Choices are 
    email, file, int, time, password
    outward = This is the word used to present to the user
    to stop adding more items.
    This would be used for a input item that you would
    want to add to a list.
    Requires: doesn't require any special imports
    """
    print(
      f'\n{c.PURPLE}{c.BOLD}'
      f'{subject.capitalize()}{c.END}\n'
      f'You can add as many items as you like.\n'
      f'But you must add at least 1 item.\n'
      f'When your done adding, Type ' 
      f'{c.RED}{c.BOLD}{outword}{c.END}\n'
    )
    item_list = []
    while True:
      item: str = input(f"Enter the {subject} {description}: ")
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
        item: str = input(f"Enter the {subject} {description}: ")
      if ((
        item == outword or 
        item == outword.capitalize() or 
        item == outword.upper()) and
        len(item_list) != 0
        ):
        length = len(item_list)
        print(
          f'\nYou have added {length} item(s), ' 
          f'Because you typed {c.RED}{c.BOLD}{item}{c.END}\n'
          f'That will complete your selection for "{subject.capitalize()}".')
        break
      else:
        print(f'You added {c.CYAN}{item}{c.END}')
        item_list.append(item)
      print(f'{c.CYAN}{item_list}{c.END}')
    return item_list

  def input_single(
    self,
    in_message: str,
    in_type: str ='email',
    fdest: str = 'home',
    max_number: int = 200
    ):
    """
    in_message = the message you want in your input string,
    in_type = the type of input field. Choices are 
    email, file, int, time, password
    This is for a single item input. This uses "validate_input"
    to verify that items entered meet requirements for that type of input
    """
    if in_type == 'int' or in_type == 'float':
      item = input(f'{in_message}(Max {max_number}): ')
    else:
      item = input(f'{in_message}: ')
    while (self.validate_input(
      item = item, 
      in_type = in_type,
      fdest = fdest,
      max_number = max_number
      ) == False):
      print(
        f'{c.RED}{c.BOLD}'
        f'This is not a valid {in_type}{c.END}')
      if in_type == 'int' or in_type == 'float':
        item = input(f'{in_message}(max {max_number}): ')
      else:
        item = input(f'{in_message}: ')
    if in_type == 'password':
      print(f'{c.CYAN}******{c.END}')
    else:
      print(f'You entered {c.CYAN}{item}{c.END}')
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
      print(f"{c.BOLD}{key}{c.END} = {c.YELLOW}{c.BOLD}{value}{c.END}")
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
    email, file, password, int, float, time
    in_type = The type of data it is suposed to be,
    max_number = the max number that can be ablied this if for int only.
    Takes the input and checks to see if it is 
    valid for its data type.
    """
    if in_type == 'email':
      print(item)
      regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
      if (search(regex,item)):
        return True
      else:
        return False
    elif in_type == 'ip':
      print(item)
      regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
      if (search(regex,item)):
        return True
      else:
        return False
    elif in_type == 'zip':
      print(item)
      regex = "\d\d\d\d\d"
      if (search(regex,item)):
        return True
      else:
        return False
    elif in_type == 'file':
      if not item:
        return False
      else:
        return fi.check_file_dir(item, fdest)
    elif in_type == 'password':
      if not item:
        return False
    elif in_type == 'time':
      try:
        datetime.strptime(item,'%H:%M').time()
        return True
      except ValueError:
        return False
    elif in_type == 'int':
      try:
        number = int(item)
        if (number <=0) or (number > max_number):
          return False
        return True
      except Exception:
        return False
    elif in_type == 'float':
      try:
        number = float(item)
        if (number <=0) or (number > max_number):
          return False
        return True
      except Exception:
        return False
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
  