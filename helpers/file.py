from datetime import datetime
from subprocess import check_output, run
from os import stat, path, mkdir, remove
import sys



class Location():

  def home_dir(self):
    home = path.expanduser('~')
    return home

  def get_resource_path(self,rel_path):
    dir_of_py_file = path.dirname(sys.argv[0])
    rel_path_to_resource = path.join(dir_of_py_file, rel_path)
    abs_path_to_resource = path.abspath(rel_path_to_resource)
    return abs_path_to_resource

class FileInfo():

  def check_file_age(
    self,
    fname, 
    fdest='relative'
    ):
    """
    Returns the difference of the current timestamp and the
    timestamp of a file last write in hours 
    Arguments = filename from home dir
    Requires import os
    """
    loc = Location()
    home = loc.home_dir()
    if fdest == 'home' or fdest == 'Home':
      file_info= stat(f'{home}/{fname}')
    else:
      file_info= stat(Location.get_resource_path(fname))
    now = datetime.now().timestamp()
    modified = int(file_info.st_mtime)
    difference_hour = int(((now - modified)/60)/60)
    return difference_hour

  def check_dir(
    self,
    dname: str, 
    ddest: str = 'home'
    ):
    """
    dname = name of the file or folder,
    ddest = the destination, either home or relative to CWD
    check to see if specified dir exists.
    Requires import os
    """
    loc = Location()
    home = loc.home_dir()
    if ddest == 'home' or ddest == 'Home':
      dpath = f'{home}/{dname}'
    else:
      dpath = Location.get_resource_path(dname)
    dir_exist = path.isdir(dpath)
    return dir_exist

  def check_file_dir(
    self,
    fname: str, 
    fdest: str = 'home'
    ):
    """
    fname = name of the file or folder,
    fdest = the destination, either home or relative to CWD
    Check if file or folder exist returns True or False
    Requires import os
    """
    loc = Location()
    home = loc.home_dir()
    if fdest == 'home' or fdest == 'Home':
      fpath = f'{home}/{fname}'
    else:
      fpath = Location.get_resource_path(fname)
    file_exist = path.exists(fpath)
    return file_exist

  def command_var(
    self, 
    in_command: str,
    ):
    """
    in_command = terminal command to run,\n
    returns the result of the command with 
    ending white space removed
    """
    com = []
    for i in in_command.split():
      com.append(i)
    try:
      raw_command = check_output(com).decode('utf-8')
      command = raw_command.strip()
      return command
    except Exception as e:
      print(e)
      return "Command Not Found"


class FileEdit():

  def make_dir(
    self,
    dname:str, 
    ddest: str = 'home'
    ):
    """
    dname = name of the file or folder,
    ddest = the destination, either home or relative to CWD
    Makes the dir specified.
    Requires import os
    """
    loc = Location()
    home = loc.home_dir()
    if ddest == 'home' or ddest == 'Home':
      mkdir(f'{home}/{dname}')
    else:
      mkdir(Location.get_resource_path(dname))


  def remove_file(
    self,
    fname:str, 
    fdest: str = 'home'
    ):
    """
    fname = name of the file or folder,
    fdest = the destination, either home or relative to CWD
    Removes the file specified
    Requires import os
    """
    loc = Location()
    home = loc.home_dir()
    if fdest == 'home' or fdest == 'Home':
      remove(f'{home}/{fname}')
    else:
      remove(Location.get_resource_path(fname))

if __name__ == "__main__":
  pass
