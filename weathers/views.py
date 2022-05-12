from django.http import JsonResponse
from .keys import appid
from django.shortcuts import render
import requests
import json
from django.core.exceptions import BadRequest


def weather(request):
    return render(request, "weathers/weather.html")

#TODO refactoring 
def weather_direct_api(request):
    if request.method == "POST":
        body = json.loads(request.body)
        query = body.get("query")

        url = "https://api.openweathermap.org/geo/1.0/direct"
        options = dict(q=query)
        response = weather_request(url, options)
        if not len(response):
            raise BadRequest
        return JsonResponse(response, safe=False)


def weather_onecall_api(request):
    if request.method == "POST":
        body = json.loads(request.body)

        url = "https://api.openweathermap.org/data/2.5/onecall"
        options = dict(lat=body.get("lat", 54.87), lon=body.get("lon", 69.16))

        response = weather_request(url, options)
        return JsonResponse(response)


def weather_request(url, options):
    params = dict(limit=1, lang="ru", units="metric", appid=appid)

    params.update(options)

    response = requests.get(url=url, params=params)

    data = response.json()
    return data
