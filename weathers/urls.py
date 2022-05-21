from django.urls import path

from . import views

app_name = "weathers"
urlpatterns = [
    path("weather", views.WeatherView.as_view(), name="weather"),
    path("weather/forecast", views.weather_forecast_api),
    path("weather/search", views.weather_search_api),
]
