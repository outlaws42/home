#! /usr/bin/env python3

# -*- coding: utf-8 -*-
from datetime import datetime
# import geopy.geocoders
from geopy.geocoders import Nominatim
import logging
import requests
from  helpers.io import IO
from helpers.dict_list import DictList
from config.instance.config import OWM_API_KEY as key
logging.basicConfig(
    filename='wu.log', 
    level=logging.INFO, 
    format='%(asctime)s %(message)s', 
    datefmt='%m/%d/%Y %I:%M:%S %p')

io = IO()
dl = DictList()

class Weather():
    degree_sign = '\N{DEGREE SIGN}'

    def __init__(self):
        pass

    def get_forecast(self):
        forecast_l = []
        dl.add_to_list(self.forecast_days(len(self.forecast_in['daily'])),forecast_l)
        dl.add_to_list(self.forecast_temp(len(self.forecast_in['daily'])),forecast_l)
        dl.add_to_list(self.forecast_precip_day(len(self.forecast_in['daily'])),forecast_l)
        dl.add_to_list(self.forecast_code(len(self.forecast_in['daily'])),forecast_l)
        dl.add_to_list(self.forecast_datetime(),forecast_l)
        return forecast_l
    

    def geolocation(self, address): 
        try:
            geolocator = Nominatim(user_agent = "weather")
            location = geolocator.geocode(address)
            addressout = location.address
            addresslist = addressout.split(',')
            if len(address) <= 5:
                city = addresslist[0]
            else:
                city = addresslist[2]
            return location.latitude, location.longitude, city
        except Exception as e:
            return 41.232921, -85.649106, "columbia city"

    def get_weather_info(
        self, 
        use_api: bool, 
        zip_code: str, 
        units: str 
        ):
        for_file ='forecast.json'
        cur_file = 'current.json'
        # location = self.geolocation(ZIP_CODE)
        # lat, long, self.city = location
        lat = 41.232921
        long = -85.649106
        try:
            if use_api == True:
                c = requests.get(f'https://api.openweathermap.org/data/2.5/weather?zip={zip_code},us&units={units}&appid={key}')
                f = requests.get(f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={long}&units={units}&exclude=current,alert,minutely,hourly&appid={key}')
                current = c.json()
                forecast = f.json()
                io.save_json(cur_file, current, 'relative')
                io.save_json(for_file, forecast, 'relative')
                self.current = io.open_json(cur_file,'relative')
                self.forecast_in = io.open_json(for_file,'relative')
            else:
                self.current = io.open_json(cur_file, 'relative')
                self.forecast_in = io.open_json(for_file,'relative')
        except Exception as e:
           self.current = io.open_json(cur_file, 'relative')
           self.forecast_in = io.open_json(for_file,'relative')
           print(f"Collect current error: {str(e)}")
           logging.info('Collect current error:  ' + str(e))
           pass
        
    def gleen_info(self):
        # weather service
        # left weather info
        # brief description of the weather
        status = {'current_status': self.current['weather'][0]['main']}
        description = {'current_description': self.current['weather'][0]['description']}
        city = {'current_city': self.current['name']}
        timezone = self.current['timezone'] # Seconds from UTC
        timezone_hour = {'current_timezone':((timezone/60)/60)} # Hours from UTC
        refresh = {'updated': datetime.utcnow()}

        # outside temp .
        outdoor_temp = {'current_temp': round(self.current['main']['temp'])}

        # wind
        import_wind_dir = self.current['wind']['deg']
        wind_dir = {'current_wind_dir': self.degtocompass(import_wind_dir)}
        wind_speed = {'current_wind_speed': round(
            self.current['wind']['speed'])}
        try:
          wind_gust = {'current_wind_gust': round(
            self.current['wind']['gust'])}
        except:
          wind_gust = {'current_wind_gust': 0}

        # Humidity
        humidity = {
            'current_humidity': f"{round(self.current['main']['humidity'])}%"}
        
        # Atmospheric Pressure
        pressure = {'current_pressure': self.current['main']['pressure']} #  hPa


        # Feels Like
        feels_like = {'current_feels_like': round(
            float(self.current['main']['feels_like']))}

        # Sun Rise/Sun Set
        sun_rise = {'current_sunrise': self.current['sys']['sunrise']}
        sun_set = {'current_sunset': self.current['sys']['sunset']}

        # Visibility
        visibility = {'visibility': self.current['visibility']}

        # Current Icon
        current_icon = {'current_icon': self.current['weather'][0]['id']}
        return [
          status,
          description,
          city,
          timezone_hour, 
          outdoor_temp, 
          refresh, 
          wind_dir, 
          wind_speed, 
          wind_gust, 
          humidity,
          pressure, 
          feels_like, 
          current_icon, 
          sun_rise, 
          sun_set, 
          visibility,
        ]

    def degtocompass(self, degrees):
        direction = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW",
                     "N"]
        val = int((degrees / 22.5) + .5)
        return direction[(val % 16)]

    def forecast_days(self, days =3):
        # forecast day for 3 days
        forecast_day = []
        for i in range(days):
            tstamp = self.forecast_in['daily'][i]['dt']
            day = {f'day{i}_dow' : datetime.fromtimestamp(tstamp).strftime('%a')}
            forecast_day.append(day)
        return forecast_day
        
    def forecast_temp(self, days = 3):
        # forecast high / low temp for 3 days    
        forecast = []
        for i in range(days):
            temp = {
                f"day{i}_temp_high" : round(self.forecast_in['daily'][i]['temp']['max']), 
                f"day{i}_temp_low": round(self.forecast_in['daily'][i]['temp']['min'])
            }
            forecast.append(temp)
        return forecast
    
    def forecast_code(self, days = 3):
        # forecast code is day / night key word starting at index 0 for 3 days
        forecast_day_code = []
        for i in range(days):
            temp = {f'day{i}_icon' : self.forecast_in['daily'][i]['weather'][0]['id']}
            forecast_day_code.append(temp)
        return forecast_day_code
        
    def forecast_precip_day(self, days=3):
        # pop is day night chance of precip starting at index 0 for 3 days
        forecast_pr = []
        for i in range(days):
            temp = self.forecast_in['daily'][i]['pop']
            temp_calc = (float(temp)*100)
            forecast_pr.append({f'day{i}_pop' : f'{int(temp_calc)}%'})
        return forecast_pr
        
    def forecast_datetime(self):
        # pop is day night chance of precip starting at index 0 for 3 days
        forecast_dt = [{"date" : datetime.utcnow(), 'replace': 1}]
        return forecast_dt

if __name__ == "__main__":
    app = Weather()
