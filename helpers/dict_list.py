from collections import ChainMap

class DictList():

  def add_to_list(list_in,list_out):
      # takes a list of items
    for i in range(len(list_in)):
      list_out.append(list_in[i])
    return list_out

  def combine_dict(dict_list):
          """
          Takes a list of dictionaries 
          and combines into one dictionary
          requires from collections import ChainMap 
          and python 3.3 or later
          """
          current = dict(ChainMap(*dict_list))
          return current