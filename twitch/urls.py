from django.urls import path

from . import views

app_name = "twitch"
urlpatterns = [
    path("twitch", views.streamers_view, name="twitch"),
    path("twitch/channels", views.streamers_api)
]
