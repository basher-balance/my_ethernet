from django.urls import path

from . import views

app_name = "vk"
urlpatterns = [
    # страница вконтакте
    path("vk", views.vk, name="vk"),
    path("hidden_post/<int:pk>", views.hidden_post, name="hidden_post"),
    path("delete_post", views.delete_post, name="delete_post"),
]
