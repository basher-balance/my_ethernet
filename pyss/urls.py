from django.urls import path
from . import views


app_name = "pyss"
urlpatterns = [
    path("", views.home, name="home"),
]
