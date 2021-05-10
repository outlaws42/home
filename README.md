# Home API

I previously wrote the weather kiosk using a raspberry pi with a display to display weather information.
This has a bit of a different purpose. This will take information from a weather API (Currently OWM) and gleen what information I want.
It will then present this information through a fastAPI for the local network to consume. 
For me the main display is going to be similar display  with a 5" or 6" screen that will set 
on a desk. 
This time I am thinking this display will be a retired phone mounted in a frame running a flutter frontend.

Separating the frontend from the backend allows for any frontend that can read the created API and display it differently depending on the device it is running on.

Right now I am really working on this and it is changing all the time. Currently it just runs a fastAPI server. It is really not ready for being used for production but if you want to use the code and or expand on it go for it.

## Prerequisites

requires: python 3.3, Open Weather Map api key, mongoDB database. It also requires tmod.py 
in the weather folder. I remove this from the repos because it was getting hard to maintain. you can get tmod from https://github.com/outlaws42/tmod.

## config.py
You will need to create a dir in config called instance and put in your config.py.  So it will be like this config/instance/config.py 
You can get a api key from https://openweathermap.org/  Alternatively you can use the weather bit API https://www.weatherbit.io/. To use weather bit you would need to change the `API` setting in the `settings.py` to 1 as well as get a weather bit API key and put it in the `config.py` file as follows. 

```python

OWM_API_KEY = 'your_OWM_api_key'
WEATHER_BIT_API_KEY = 'your_weatherbit_api_key'

```

## Installing 

Installing python 3, pip on the raspberry pi or any debian based linux computer
```bash
sudo apt-get install python3 python3-pip 

```
Run this from a terminal in the dir you want. to clone the repo to your local computer

```bash
git clone https://github.com/outlaws42/home.git


```
Change into the project main dir

```bash
cd home

```

Then run this command to install the modules needed

```bash
pip3 install -r requirements.txt

```

You will have to make the python files executable.

```bash
chmod u+x *.py

```

## To run
**get_weather.py** will check the weather API every 15 min. This is the main file that
collects the information for the weather kiosk API.

**sensor_sub.py** Is set to subscribe to MQTT broker. On my network it gets the status of a Garage door and and a indoor temp sensor. It could be configured to subscribe to anything you are publishing over MQTT 

**main.py** serves up the fastAPI API for your front end. 

The best way to run these is to make these a system service that starts at boot time. 

Besides these 3 you will need a system service for the mongoDB database. In Linux that uses systemd this is `sudo systemctl enable mongod.service` to enable the installed
mongoDB database to start at boot time.  To install MongoDB server community Edition on Ubuntu Linux you can follow these instructions. [Install MongoDB in Ubuntu](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/)   

```bash
./get_weather.py
./sensor_sub.py
./main.py

```

**Note:** You should be able to run this code on Windows and MacOS as well as long as you have the 
prerequisites installed. Running the python files and starting everything at boot time will be different for those platforms but it should be possible.

## db_convert.py & past_cli.py

These 2 files are not needed for the normal running of the server. I used **db_convert.py** to convert an old data dump from a sql database to the mongoDB database. I use  **past_cli.py** to get the days high low temp for the date specified if there is a issue for some reason that the automatic high low collection failed. This is rare but it is a tool that can be used to run and collect the high and low for the day specified and write to the past collection in the database.

## Example API Calls

### /weather/current
```json
{
  "current": {
    "visibility": 10000,
    "current_sunset": 1616284457,
    "current_sunrise": 1616240721,
    "current_icon": 800,
    "current_feels_like": 21,
    "current_pressure": 1037,
    "current_humidity": "76%",
    "current_wind_gust": 4,
    "current_wind_speed": 1,
    "current_wind_dir": "ENE",
    "updated": 1616239686,
    "current_temp": 27,
    "current_timezone": -4,
    "current_city": "Larwill",
    "current_description": "clear sky",
    "current_status": "Clear"
  }
}

```

### /weather/forecast

```json
{
  "forecast": {
    "date": 1616239686,
    "day7_icon": 500,
    "day6_icon": 800,
    "day5_icon": 501,
    "day4_icon": 500,
    "day3_icon": 501,
    "day2_icon": 802,
    "day1_icon": 800,
    "day0_icon": 800,
    "day7_pop": "51%",
    "day6_pop": "8%",
    "day5_pop": "100%",
    "day4_pop": "100%",
    "day3_pop": "100%",
    "day2_pop": "0%",
    "day1_pop": "0%",
    "day0_pop": "0%",
    "day7_temp_high": 61,
    "day7_temp_low": 34,
    "day6_temp_high": 50,
    "day6_temp_low": 32,
    "day5_temp_high": 44,
    "day5_temp_low": 40,
    "day4_temp_high": 60,
    "day4_temp_low": 48,
    "day3_temp_high": 55,
    "day3_temp_low": 49,
    "day2_temp_high": 60,
    "day2_temp_low": 41,
    "day1_temp_high": 58,
    "day1_temp_low": 35,
    "day0_temp_high": 53,
    "day0_temp_low": 28,
    "day7_dow": "Sat",
    "day6_dow": "Fri",
    "day5_dow": "Thu",
    "day4_dow": "Wed",
    "day3_dow": "Tue",
    "day2_dow": "Mon",
    "day1_dow": "Sun",
    "day0_dow": "Sat"
  }
}

```
### /weather/past/day or /weather/past/year
Current is past day and past year for these to work you have have this data in 
database or it will return no data.

```json
{
    "forecast_day": {
        "icon": 500,
        "high": 42,
        "low": 27,
        "date": 1609304400
    }
}

// forecast year
{
    "forecast_year": {
        "icon": 804,
        "high": 31,
        "low": 25,
        "date": 1577768400
    }
}


```

### /house/sensors/frtemp or /house/sensors/gdbasement
These sensors are more specific to my setup but is an example
of the sensors API.

```json
{
  "sensors": {
    "sensor": "frtemp",
    "sensor_val": 69,
    "dt": 1616240385
  }
}


{
  "sensors": {
    "sensor": "gdbasement",
    "sensor_val": 0,
    "dt": 1616240587
  }
}


```


## Author

Troy Franks

## License

GPL
 
