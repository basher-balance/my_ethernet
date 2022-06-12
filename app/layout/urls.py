from django.urls import path
from . import views


app_name = "layout"
urlpatterns = [
    path("", views.layout, name="layout"),
]
