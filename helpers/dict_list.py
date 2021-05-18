from collections import ChainMap

class DictList():

  def add_to_list(
    list_in: list,
    list_out: list
  ):
    """ 
    list_in = list of items,
    list_out = list you are adding to.
    takes a list of items and 
    adds it to another list
    """
    for i in range(len(list_in)):
      list_out.append(list_in[i])
    return list_out

  def combine_dict(dict_list: list):
          """
          Takes a list of dictionaries 
          and combines into one dictionary
          requires from collections import ChainMap 
          and python 3.3 or later
          """
          current = dict(ChainMap(*dict_list))
          return current

  def dict_to_list(dictionary: dict):
    """
    Convert dictionary to a list
    """
    temp = []
    list_name = []
    for key, value in dictionary.items():
      temp = [key,value]
      list_name.append(temp)
    return list_name.sort()

def group_list(
  lname: list, 
  positions: int, 
  start: int = 0
  ):
  """
  lname = list of items,
  positions = number of positions in the sublist,
  start = item to start with. 
  takes a list and groups them into 
  sub lists in the amount of positions
  """
  while start <= len(lname) - positions:
    yield lname[start:start + positions]
    start += positions

if __name__ == "__main__":
  app = DictList()
