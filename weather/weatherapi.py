#! /usr/bin/env python3

# -*- coding: utf-8 -*-
from datetime import datetime
import logging
import requests
import weather.tmod as tmod
from config.instance.config import WEATHER_API_API_KEY as key
from config.settings import USE_API, ZIP_CODE
logging.basicConfig(
    filename='wu.log',
    level=logging.INFO,
    format='%(asctime)s %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p')


class Weather():
    degree_sign = '\N{DEGREE SIGN}'

    def __init__(self):
        pass

    def get_forecast(self):
        forecast_l = []
        tmod.add_to_list(self.forecast_days(
            len(self.forecast_in['forecast']['forecastday'])), forecast_l)
        tmod.add_to_list(self.forecast_temp(
            len(self.forecast_in['forecast']['forecastday'])), forecast_l)
        tmod.add_to_list(self.forecast_precip_day(
            len(self.forecast_in['forecast']['forecastday'])), forecast_l)
        tmod.add_to_list(self.forecast_code(
            len(self.forecast_in['forecast']['forecastday'])), forecast_l)
        tmod.add_to_list(self.forecast_datetime(), forecast_l)
        return forecast_l

    def get_weather_info(self):
        # USE_API = False
        print('WeatherApi')
        try:
            if USE_API == True:
                f = requests.get(
                    (f'https://api.weatherapi.com/v1/forecast.json?'
                     f'key={key}&q={ZIP_CODE}&days=3&aqi=no&alerts=no')
                )
                forecast = f.json()
                # tmod.save_json('current.json', current, 'relative')
                tmod.save_json('forecastwa.json', forecast, 'relative')
                # self.current = tmod.open_json('current.json','relative')
                self.forecast_in = tmod.open_json(
                    'forecastwa.json', 'relative')
                print(f"USE_API: {USE_API}")
            else:
                print(f"USE_API: {USE_API}")
                # self.current = tmod.open_json('current.json', 'relative')
                self.forecast_in = tmod.open_json(
                    'forecastwa.json', 'relative')
        except Exception as e:
            #    self.current = tmod.open_json('current.json', 'relative')
            self.forecast_in = tmod.open_json('forecastwa.json', 'relative')
            print(f"Collect current error: {str(e)}")
            logging.info('Collect current error:  ' + str(e))
            pass
    
    def gleen_info(self):
        # weather service
        # left weather info
        # brief description of the weather
        status = {'current_status': 
        self.forecast_in['current']['condition']['text']}
        description = {'current_description': 
        self.forecast_in['current']['condition']['text']}
        city = {'current_city': self.forecast_in['location']['name']}
        timezone = self.forecast_in['location']['localtime_epoch'] # Seconds from UTC
        timezone_hour = {'current_timezone':((timezone/60)/60)} # Hours from UTC
        refresh = {'updated': datetime.utcnow()}

        # outside temp .
        outdoor_temp = {'current_temp': round(self.forecast_in['current']['temp_f'])}

        # wind
        import_wind_dir = self.forecast_in['current']['wind_degree']
        wind_dir = {'current_wind_dir': self.degtocompass(import_wind_dir)}
        wind_speed = {'current_wind_speed': round(
            self.forecast_in['current']['wind_mph'])}
        try:
          wind_gust = {'current_wind_gust': round(
            self.forecast_in['current']['gust_mph'])}
        except:
          wind_gust = {'current_wind_gust': 0}

        # Humidity
        humidity = {
            'current_humidity': f"{round(self.forecast_in['current']['humidity'])}%"}
        
        # Atmospheric Pressure
        pressure = {'current_pressure': self.forecast_in['current']['pressure_in']} #  hPa


        # Feels Like
        feels_like = {'current_feels_like': round(
            float(self.forecast_in['current']['feelslike_f']))}

        # Sun Rise/Sun Set
        sun_rise = {'current_sunrise': tmod.timestamp_from_string_time(
            self.forecast_in['forecast']['forecastday'][0]['astro']['sunrise'])}
        sun_set = {'current_sunset': tmod.timestamp_from_string_time(
            self.forecast_in['forecast']['forecastday'][0]['astro']['sunset'])}

        # Visibility
        visibility = {'visibility': self.forecast_in['current']['vis_miles']}

        # Current Icon
        current_icon = {'current_icon': self.condition_codes(
            self.forecast_in['current']['condition']['code'])}
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

    def forecast_days(self, days=3):
        # forecast day for 3 days
        forecast_day = []
        for i in range(days):
            tstamp = self.forecast_in['forecast']['forecastday'][i]['hour'][0]['time_epoch']
            print(tstamp)
            day = {f'day{i}_dow': datetime.fromtimestamp(
                tstamp).strftime('%a')}
            forecast_day.append(day)
        return forecast_day

    def forecast_temp(self, days=3):
        # forecast high / low temp for 3 days
        forecast = []
        for i in range(days):
            temp = {
                f"day{i}_temp_high": 
                round(self.forecast_in['forecast']['forecastday'][i]['day']['maxtemp_f']),
                f"day{i}_temp_low": 
                round(self.forecast_in['forecast']['forecastday'][i]['day']['mintemp_f'])
            }
            forecast.append(temp)
        return forecast

    def forecast_code(self, days=3):
        # forecast code is day / night key word starting at index 0 for 3 days
        forecast_day_code = []
        for i in range(days):
            temp = {f'day{i}_icon':
                    self.condition_codes(self.forecast_in['forecast']['forecastday']
                    [i]['day']['condition']['code'])
                    }
            forecast_day_code.append(temp)
        return forecast_day_code

    def forecast_precip_day(self, days=3):
        # pop is day night chance of precip starting at index 0 for 3 days
        forecast_pr = []
        for i in range(days):
            temp = (
                self.forecast_in['forecast']
                ['forecastday'][i]['day']
                ['daily_chance_of_rain'])
            # temp_calc = (float(temp)*100)
            forecast_pr.append({f'day{i}_pop': f'{temp}%'})
        return forecast_pr

    def forecast_datetime(self):
        # pop is day night chance of precip starting at index 0 for 3 days
        forecast_dt = [{"date": datetime.utcnow(), 'replace': 1}]
        return forecast_dt

    def condition_codes(self, code):
        clear = [1000]
        fog = [1135, 1147]
        cloudy = [1006, 1009]
        snow = [
            1066, 1072, 1168, 1171, 1198, 1201, 1204, 
            1207, 1237, 1249, 1252, 1261, 1264, 1210,
            1213, 1216, 1222, 1225, 1255, 1258, 1117, 1114
        ]
        rain = [
            1030, 1063, 1186, 1189, 1192, 1195, 1240, 
            1243, 1246, 1150, 1153, 1183, 1187, 1273,
            1276, 1279, 1282
        ]
        partly_cloudy =[1003]
        if code in clear:
            ad_code = 800
            return ad_code
        elif code in fog:
            ad_code = 741
            return ad_code
        elif code in cloudy:
            ad_code = 804
            return ad_code
        elif code in snow:
            ad_code = 601
            return ad_code
        elif code in rain:
            ad_code = 501
            return ad_code
        elif code in partly_cloudy:
            ad_code = 801
            return ad_code
        else:
            return 0


if __name__ == "__main__":
    app = Weather()
