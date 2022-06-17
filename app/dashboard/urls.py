from django.urls import path
from . import views


app_name = "dashboard"
urlpatterns = [
    path("dashboard", views.get_undetected_anime, name="dashboard"),
    # path(
    #     "delete_from_anime_parse_list",
    #     views.delete_anime,
    #     name="delete_from_anime_parse_list",
    # ),
]
