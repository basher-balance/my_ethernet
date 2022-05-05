from django.urls import path

from . import views

app_name = "serials"
urlpatterns = [
    path("serials", views.get_fresh_serials, name="serials"),
    path("hiden_serial/<int:pk>", views.hidden_serial, name="hidden_serial"),
]
