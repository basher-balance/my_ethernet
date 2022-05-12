from django.http import JsonResponse
from .keys import appid
from django.shortcuts import render, redirect
import requests


url = "https://api.openweathermap.org/data/2.5/onecall"

params = dict(
    lat=54.87, lon=69.16, exlude="dayliy", lang="ru", units="metric", appid=appid
)


def weather(request):
    return render(request, "weathers/weather.html")


def open_weather_api(req):
    if req.method == "GET":
        payload = requests.get(url=url, params=params)
        data = payload.json()
        return JsonResponse(data)
