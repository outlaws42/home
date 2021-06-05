from datetime import datetime, date, time
from pytz import timezone

class DT():

  def check_str_date_format(
    self, 
    str_date: str, 
    format: str = '%Y-%m-%d'
    ):
    """
    str_date = takes a string date,
    returns True or False depending if
    passed str date fits the format.
    """
    try:
      dt_status = bool(datetime.strptime(str_date, format))
      return dt_status
    except ValueError as e:
      return False

  def check_str_time_format(
    self, 
    str_time: str, 
    format: str = '%H:%M'
    ):
    """
    str_time = takes a string time,
    format = "%H:%M" (24 hour zero padded time), 
    "%I:%M %p" (12 hour zero padded)
    returns True or False depending if
    passed str time fits the format.
    """
    try:
      dt_status = bool(datetime.strptime(str_time, format))
      return dt_status
    except ValueError as e:
      return False


  def day_diff(
    self,
    month: int,
    day:int,
    year: int
    ):
    """
    Takes month day year and 
    gets the difference from
    current date
    """
    current = date.today()
    day = date(year,month,day)
    till_day = day - current
    return till_day.days

  def year_current(self):
    """
    Returns the current year
    """
    current = date.today()
    current_year = current.year
    return current_year

  def from_str_time(
    self,
    str_time: str, 
    timestamp: bool = False, 
    utc: bool = False, 
    tzone: str = 'US/Eastern',
    format: str = '%H:%M'
    ):
    """ 
    str_time = "HH:MM" based on 24 hour clock
    or "HH:MM am/pm" based on 12 hour clock,\n 
    timestamp = True or False,
    False: returns datetime object today at that time
    True: returns timestamp today at that time\n 
    utc = True or False,
    True:  sets timezone to UTC, 
    False: sets timezone to local timezone\n 
    tzone = Sets the timezone default 'US/Eastern'\n
    format = This is the format of the str_time\n 
    Example: '%H:%M' would be format for 24 hour clock\n
    Example: '%I:%M %p' would be format for 12 hour clock 
    with am or pm, add '%S' for seconds\n
    Requires from datetime import datetime, date, time / 
    from pytz import timezone
    """
    check = self.check_str_time_format(str_time,format)
    if check == False:
      return "String time doesn't fit the format given"
    if utc:
      tz =timezone('UTC')
    else:
      tz = timezone(tzone)
    dt_time = datetime.strptime(str_time, format).time() 
    dt = datetime.combine(date.today(), dt_time)
    dttz = tz.localize(dt)
    if timestamp:
      ts = int(dttz.timestamp())
      return ts
    else:
      return dttz

  def str_date_from_datetime(self,dt: datetime):
    """ Datetime return string date
        Requires from datetime import datetime
    """
    str_date = dt.strftime('%Y-%m-%d')
    return str_date

  def from_str_date(
    self,
    str_date: str,
    timestamp: bool = False,
    utc: bool = False,
    tzone: str = 'US/Eastern'
    ): 
    """ Pass string date YYYY-MM-DD, timestamp = True or False,
        utc = True or False, timezone = 'US/Eastern'
        timestamp = False returns datetime object current time at that date,
        timestamp = True returns timestamp current time at that date
        utc = True  sets timezone to UTC, False sets timezone to local timezone
        Requires from datetime import datetime, date, time / 
        from pytz import timezone
    """
    dt_validation = self.check_str_date_format(str_date)
    if dt_validation == False:
      message = ( f'This is not a correct date string ' 
      f'following YYYY-MM-DD You entered {str_date}')
      return message
    if utc:
      tz =timezone('UTC')
    else:
      tz = timezone(tzone)
    date_request = str_date
    year, month, day = date_request.split('-')
    tm = datetime.now(tz).time()
    dt = datetime.combine(
      date(int(year), int(month), int(day)), tm)
    dttz = tz.localize(dt)
    if timestamp:
      ts = int(dttz.timestamp())
      return ts
    else:
      return dttz

  def from_datetime(
    self, 
    dt: datetime,
    timestamp: bool = False, 
    format: str = '%H:%M'
    ):
    """
    dt = datetime\n
    timestamp = True returns timestamp
    False returns string time or date default(False) 
    format = format you want the string 
    time or date to be in Default(%H:%M).\n
    24 hour time = '%H:%M', 
    12 hour = '%I:%M %p'\n
    common date = '%Y-%m-%d' (YYYY-MM-DD) 
    """
    if type(dt) is not datetime:
      return "Input is not a datetime object"

    if timestamp == True:
      output = int(datetime.timestamp(dt))
    else:
      output = datetime.strftime(dt, format)
    return output
  
  def from_timestamp(
    self, 
    ts,
    dt: bool = False, 
    format: str = '%H:%M'
    ):
    """
    ts = timestamp\n 
    dt = True return datetime object, 
    False return string date or time.\n
    format = format you want the string 
    time or date to be in Default(%H:%M).\n
    24 hour time = '%H:%M', 
    12 hour = '%I:%M %p'\n
    common date = '%Y-%m-%d' (YYYY-MM-DD) 
    """
    # if type(ts) is not timestamp:
    #   return "Input is not a datetime object"
    try:
      dtout = datetime.fromtimestamp(ts) 
    except Exception:
      return "Not a valid datetime"
    if dt == True:
      return dtout
    str_dt = datetime.strftime(dtout, format)
    return str_dt    

if __name__ == "__main__":
  app = DT()
