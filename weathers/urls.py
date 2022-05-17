from django.urls import path

from . import views

app_name = "weathers"
urlpatterns = [
    # страница погоды
    path("weather", views.WeatherView.as_view(), name="weather"),
    path("weather/forecast", views.weather_onecall_api),
    path("weather/search", views.weather_direct_api),
]
