from django.http import JsonResponse
from .keys import appid
from django.shortcuts import render, redirect
import requests
import json


def weather(request):
    return render(request, "weathers/weather.html")


def weather_api(request):
    if request.method == "POST":
        body = json.loads(request.body)
        lat = body.get("lat", 54.87)
        lon = body.get("lon", 69.16)

        url = "https://api.openweathermap.org/data/2.5/onecall"
        params = dict(
            lat=lat,
            lon=lon,
            # exclude="daily",
            lang="ru",
            units="metric",
            appid=appid,
        )

        payload = requests.get(url=url, params=params)
        data = payload.json()
        return JsonResponse(data)
