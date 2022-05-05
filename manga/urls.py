from django.urls import path

from . import views

app_name = 'manga'
urlpatterns = [
    path('manga', views.get_manga, name='manga'),
    path('hidden_manga/<int:pk>', views.hidden_manga, name='hidden_manga'),
]
