import requests
import json

from task_scheduler.keys import appid
from django.http import JsonResponse
from django.core.exceptions import BadRequest
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView


direct_url = "https://api.openweathermap.org/geo/1.0/direct"
onecall_url = "https://api.openweathermap.org/data/2.5/onecall"


class WeatherView(TemplateView):
    template_name: str = "weathers/weather.html"


@require_POST
def weather_search_api(request):
    body = json.loads(request.body)
    query = body.get("query")
    direct_options = dict(q=query)

    direct_response = api_request(direct_url, direct_options)
    if not direct_response:
        raise BadRequest()

    weather_options = dict(
        lat=direct_response[0].get("lat"),
        lon=direct_response[0].get("lon"),
    )
    weather_response = api_request(onecall_url, weather_options)
    return JsonResponse({
        "direct": direct_response,
        "weather": weather_response,
    })


@require_POST
def weather_forecast_api(request):
    body = json.loads(request.body)
    lat = body.get("lat")
    lon = body.get("lon")
    options = dict(lat=lat, lon=lon)
    response = api_request(onecall_url, options)
    return JsonResponse(response)


def api_request(url, options):
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

    return response.json()
