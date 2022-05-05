from weathers.models import Weather, Weather_Today

import logging
import os

from .tasks import process_user_stats
import datetime
import requests
import plotly.express as px

from .keys import appid


url = 'https://api.openweathermap.org/data/2.5/onecall?lat=54.8753&lon=69.162&daily&units=metric&appid=' + appid
city = 'Petropavl'
r = requests.get(url.format(city)).json()
dt = [datetime.datetime.fromtimestamp(r['daily'][number_day]['dt']).strftime("%A %d %m") for number_day in
      range(6)]
sunrises = [datetime.datetime.fromtimestamp(r["daily"][number_day]["sunrise"]).strftime("%H %M %S") for
            number_day in range(6)]
sunsets = [datetime.datetime.fromtimestamp(r["daily"][number_day]["sunset"]).strftime("%H %M %S") for number_day
           in range(6)]
temp_mins = [r['daily'][number_day]['temp']['min'] for number_day in range(6)]
temp_maxs = [r['daily'][number_day]['temp']['max'] for number_day in range(6)]
temp_days = [r['daily'][number_day]['temp']['day'] for number_day in range(6)]
icons = [r['daily'][number_day]['weather'][0]['icon'] for number_day in range(6)]

def wdl():
    delete_weather_daily = Weather.objects.all()
    delete_weather_daily.delete()
    weather_daily_lists = [{'item1': t[0], 'item2': t[1],
                        'item3': t[2], 'item4': t[3], 'item5': t[4],
                        'item6': t[5], 'item7': t[6]}
                       for t in zip(dt, sunrises, sunsets, temp_mins, temp_maxs, temp_days, icons)]
    return weather_daily_lists


#def dd():
#    diagram_dict = {}
#    data_temp = [dt, temp_days, icons, temp_maxs, temp_mins, sunsets, sunrises]
#    fig_data_temp = px.bar(data_temp, x=dt, y=temp_days)
#    fig_data_sunsets = px.bar(data_temp, x=dt, y=sunsets)
#    fig_data_sunrises = px.bar(data_temp, x=dt, y=sunrises)
#    fig_data_icons = px.bar(data_temp, x=dt, y=icons)
#    fig_temp = fig_data_temp.to_html(full_html=False)
#    fig_sunset = fig_data_sunsets.to_html(full_html=False)
#    fig_sunrise = fig_data_sunrises.to_html(full_html=False)
#    fig_icon = fig_data_icons.to_html(full_html=False)
#    diagram_dict['temp'] = fig_temp
#    diagram_dict['sunset'] = fig_sunset
#    diagram_dict['sunrise'] = fig_sunrise
#    diagram_dict['icon'] = fig_icon
#    return diagram_dict

def weather_today():
    url_wether_today = 'https://api.openweathermap.org/data/2.5/onecall?lat=54.8753&lon=69.162&exclude=current&units=metric&appid=' + appid
    city = 'Petropavl'
    r = requests.get(url_wether_today.format(city)).json()
    delete_weather = Weather_Today.objects.all()
    delete_weather.delete()
    weather_today = Weather_Today.objects.create(
            cloud=r['daily'][0]['clouds'],
            datetime = datetime.datetime.fromtimestamp(r['daily'][0]['dt']).strftime("%A %d %m"),
            humidity = r['daily'][0]['humidity'],
            moon_phase = r['daily'][0]['moon_phase'],
            pup = r['daily'][0]['pop'],
            pressure = r['daily'][0]['pressure'],
#            rain = r['daily'][0]['rain'],
            # snow = r['daily'][0]['snow'],
            sunrise = datetime.datetime.fromtimestamp(r['daily'][0]['sunrise']).strftime("%H %M %S"),
            sunset = datetime.datetime.fromtimestamp(r['daily'][0]['sunset']).strftime("%H %M %S"),
            temp = r['daily'][0]['temp'],
            uvi = r['daily'][0]['uvi'],
            weather_description = r['daily'][0]['weather'][0]['description'],
            weather_icon = r['daily'][0]['weather'][0]['icon'],
            weather_main = r['daily'][0]['weather'][0]['main'],
            )
    weather_today.save()


def weather_pars():
    logging.warning('It is time to start the dramatiq task weather')
    '''Функция выполняющая функции'''
    weather_today()
    Weather.objects.create(weather_daily=wdl()).save()
    process_user_stats.send()
