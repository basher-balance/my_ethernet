from django.urls import path

from . import views

app_name = "anime"
urlpatterns = [
    # страница anime
    path("anime", views.get_fresh_anime, name="anime"),
    path("hidden_anime/<int:pk>", views.hidden_anime, name="hidden_anime"),
]
