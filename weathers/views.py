import requests
import json

from django.http import JsonResponse

from task_scheduler.keys import appid
from django.core.exceptions import BadRequest
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView



class WeatherView(TemplateView):
    template_name: str = "weathers/weather.html"


@require_POST
def weather_direct_api(request):
    url = "https://api.openweathermap.org/geo/1.0/direct"
    response = request_handler(request, url)
    if not len(response):
        raise BadRequest
    return JsonResponse(response, safe=False)


@require_POST
def weather_onecall_api(request):

    url = "https://api.openweathermap.org/data/2.5/onecall"
    response = request_handler(request, url)
    return JsonResponse(response)


def request_handler(req, url: str):
    body = json.loads(req.body)
    query = body.get("query")
    if "direct" in url:
        options = dict(q=query)
        response = weather_request(url, options)
        return response
    elif "onecall" in url:
        options = dict(
            lat=body.get("lat"),
            lon=body.get("lon"),
        )

        response = weather_request(url, options)
        return response


def weather_request(url, options):
    params = dict(
        limit=1,
        lang="ru",
        units="metric",
        appid=appid,
    )

    params.update(options)

    response = requests.get(
        url=url,
        params=params,
    )

    data = response.json()
    return data
