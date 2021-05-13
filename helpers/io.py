from yaml import safe_dump, safe_load
from json import dump, load
from helpers.file import Location as loc

class IO():
  def open_file(
    fname: str,
    fdest: str = 'relative', 
    def_content: str = '0',
    mode: str = 'r'
    ):
    """
    fname = filename, fdest = file destination, 
    def_content = default value if the file doesn't exist,
    mode = defines read mode 'r' or 'rb'
    Opens the file if it exists and returns the contents.
    If it doesn't exitst it creates it. Writes 
    the def_content value to it and returns the def_content value
    import os
    """
    home = loc.home_dir()
    try:
        if fdest == 'home' or fdest == 'Home':
            with open(f'{home}/{fname}', mode) as path_text:
                content=path_text.read()
        else:
            with open(loc.get_resource_path(fname), mode) as text:
                content=text.read()
        return content
    except(FileNotFoundError) as e:
        print(e)
        print('It is reading here')
        if fdest == 'home' or fdest == 'Home':
            with open(f'{home}/{fname}', 'w') as output:
                output.write(def_content)
        else:
            with open(loc.get_resource_path(fname), 'w') as output:
                output.write(def_content)
        return def_content

  def save_file(
      fname: str,
      content: str,
      fdest: str ='relative', 
      mode: str = 'w'):
      """
      fname = filename, content = what to save to the file, 
      fdest = where to save file, mode = w for write or a for append
      import os
      """
      home = loc.home_dir()
      if fdest == 'home' or fdest == 'Home':
          with open(f'{home}/{fname}', mode) as output:
              output.write(content)
      else:
          with open(loc.get_resource_path(fname), mode) as output:
              output.write(content)
  def save_file_append(file_,variable,type_='relative'):
      home = loc.home_dir()
      if type_ == 'home' or type_ == 'Home':
          with open(f'{home}/{file_}', 'a') as output:
              output.write(variable)
      else:
          with open(loc.get_resource_path(file_), 'a') as output:
              output.write(variable)

  def save_json(
    fname: str,
    content: str,
    fdest: str = 'relative'
    ):
    home = loc.home_dir()
    if fdest == 'home' or fdest == 'Home':
        with open(f'{home}/{fname}', 'w') as output:
            dump(content,output, sort_keys=True, indent=4)
    else:
        with open(loc.get_resource_path(fname), 'w') as output:
            dump(content,output, sort_keys=True, indent=4)
                
  def open_json(
    fname: str,
    fdest: str = 'relative',
    def_content = {'key': 'value'},
    ):
    """
    fname = filename, fdest = file destination, 
    def_content = default value if the file doesn't exist
    opens the file if it exists and returns the contents
    if it doesn't exitst it creates it writes 
    the def_content value to it and returns the def_content value
    requires: import os, yaml
    """
    home = loc.home_dir()
    try:
        if fdest == 'home' or fdest == 'Home':
            with open(f'{home}/{fname}', 'r') as fle:
                    content = load(fle)
            return content
        else:
            with open(loc.get_resource_path(fname), 'r') as fle:
                    content = load(fle)
            return content
    except(FileNotFoundError, EOFError) as e:
        print(e)
        if fdest == 'home' or fdest == 'Home':
            with open(f'{home}/{fname}', 'w') as output:
                dump(def_content, output, sort_keys=True, indent=4)
        else:
            with open(loc.get_resource_path(fname), 'w') as output:
                dump(def_content, output, sort_keys=True, indent=4)
        return def_content

  def save_yaml(
      fname: str,
      content: dict,
      fdest: str ='relative',
      mode: str = 'w'
      ):
      """
      fname = filename, content = data to save, fdest = file destination,
      mode = 'w' for overwrite file or 'a' to append to the file
      Takes a dictionary and writes it to file specified. it will either
      write or append to the file depending on the mode method
      requires: import os, yaml
      """
      home = loc.home_dir()
      if fdest == 'home' or fdest == 'Home':
          with open(f'{home}/{fname}', mode) as output:
              safe_dump(content,output, sort_keys=True)
      else:
          with open(loc.get_resource_path(fname), mode) as output:
              safe_dump(content,output, sort_keys=True)

  def open_yaml(
      fname: str,
      fdest: str ='relative',
      def_content: dict = {'key': 'value'}
      ):
      """
      fname = filename, fdest = file destination, 
      def_content = default value if the file doesn't exist
      opens the file if it exists and returns the contents
      if it doesn't exitst it creates it writes 
      the def_content value to it and returns the def_content value
      import os, yaml(pip install pyyaml)
      """
      home = loc.home_dir()
      try:
          if fdest == 'home' or fdest == 'Home':
              with open(f'{home}/{fname}', 'r') as fle:
                      content = safe_load(fle)
              return content
          else:
              with open(loc.get_resource_path(fname), 'r') as fle:
                      content = safe_load(fle)
              return content
      except(FileNotFoundError, EOFError) as e:
          print(e)
          if fdest == 'home' or fdest == 'Home':
              with open(f'{home}/{fname}', 'w') as output:
                  safe_dump(def_content,output, sort_keys=True)
          else:
              with open(loc.get_resource_path(fname), 'w') as output:
                  safe_dump(def_content,output, sort_keys=True)
          return def_content

  def last_n_lines(
    fname: str, 
    lines: int, 
    fdest: str ='relative'
    ):
    """
    Gets the last so many lines of a text 
    file and returns those lines in text.
    Arguments = filename, number of lines,
    file destination
    """
    home = loc.home_dir()
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
