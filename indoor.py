#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Imports ///////////////////
from time import sleep
from sensors.indoor_temp import IndoorTemp

# Refresh rate /////////////////////////////////
refresh_type = '2'  # 1 = minutes 2 = Seconds
refresh_rate_amount = 5

if refresh_type == '1':
  # Minutes Refresh (minutes*60) sleep() is in seconds
  refresh = (refresh_rate_amount*60)  
else:
  # Seconds Refresh refresh_rate_amount sleep() is in seconds
  refresh = refresh_rate_amount

class Indoor():
  run_once = 1

  def __init__(self):
    try:
      while True:
       self.main()
       sleep(refresh)
    except (KeyboardInterrupt) as e:
        print(e)
        print('Interupted')
  
  def main(self):
    self.indoor_temp = IndoorTemp()
    self.indoor_temp.run()

if __name__ == "__main__":
            app = Indoor()    
