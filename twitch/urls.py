from django.urls import path

from . import views

app_name = 'twitch'
urlpatterns = [
    path('twitch', views.get_streamer, name='twitch'),
    path('delete_streamer/<int:pk>', views.delete_streamer, name='delete_streamer'),
]
