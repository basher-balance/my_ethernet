from django.urls import path
	
from . import views

app_name = 'torrents'
urlpatterns = [
    path('torrents', views.get_fresh_torrent, name='torrents'),
    path('hiden_torrent/<int:pk>', views.hidden_torrent, name='hidden_torrent'),
]
