from os import path
from sys import argv

class Location():
  def home_dir():
    home = path.expanduser('~')
    return home

  def get_resource_path(rel_path):
    dir_of_py_file = path.dirname(argv[0])
    rel_path_to_resource = path.join(dir_of_py_file, rel_path)
    abs_path_to_resource = path.abspath(rel_path_to_resource)
    return abs_path_to_resource