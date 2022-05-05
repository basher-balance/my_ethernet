from django.urls import path
from . import views

app_name = 'pyss'

urlpatterns = [
    #Домашняя страница
    path('', views.home, name='home'),
]
