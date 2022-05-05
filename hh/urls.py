from django.urls import path
    
from . import views

app_name = 'hh'
urlpatterns = [
    path('hh', views.get_fresh_hh, name='hh'),
    path('hidden_hh/<int:pk>', views.hidden_hh, name='hidden_hh'),
]
