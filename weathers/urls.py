from django.urls import path

from . import views

app_name = "weathers"
urlpatterns = [
    # страница погоды
    path("weather", views.weather, name="weather"),
    path("weather/forecast", views.weather_request),
    path("weather/search", views.weather_onecall_api),
]
