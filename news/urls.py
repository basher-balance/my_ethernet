from django.urls import path

from . import views

app_name = "news"
urlpatterns = [
    # домашняя страница
    path("news", views.get_fresh_news, name="news"),
    # path('parse_news', views.parse_news, name='parse_news'),
    path("hiden_news/<int:pk>", views.hidden_news, name="hidden_news"),
    path("delete_news", views.delete_news, name="delete_news"),
]
