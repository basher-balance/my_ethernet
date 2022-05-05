from django.shortcuts import render, redirect
from .models import Weather, Weather_Today


def weather(request):
    '''Выводит данные из моделей Weather и Weather_Today'''
    weather_week = list(Weather.objects.all().values_list('weather_daily'))
    weather_today = list(Weather_Today.objects.values())
    #weather_diagram = list(Weather.objects.all().values_list('diagram'))
    return render(request, 'weathers/weather.html', {
        'weather_week': weather_week[0][0][1:],
        'weather_today': weather_today[0],
        #'weather_diagram': weather_diagram[0][0][1:],
        }
        )
