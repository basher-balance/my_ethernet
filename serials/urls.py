from django.urls import path

from . import views

app_name = "serials"
urlpatterns = [
    path("serials", views.get_fresh_serials, name="serials"),
    path("hiden_serial/<int:pk>", views.hidden_serial, name="hidden_serial"),
    path("del_serial/<int:pk>", views.del_serial, name="del_serial"),
    path("add_anime_parse/<int:pk>", views.add_anime_parse, name="add_anime_parse"),
    path("add_torrent/<int:pk>", views.add_torrent, name="add_torrent"),
]
