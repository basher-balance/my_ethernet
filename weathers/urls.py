from django.urls import path
	
from . import views

app_name = 'weathers'
urlpatterns = [
    # страница погоды 
    path('weather', views.weather, name='weather'),
]
