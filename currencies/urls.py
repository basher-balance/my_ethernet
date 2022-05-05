from django.urls import path
	
from . import views
	
app_name = 'currencies'
urlpatterns = [
    # Домашняя страница
    path('currency', views.currency_parse, name='currency'),
]
