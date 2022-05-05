from django.urls import path                       
                                                  
from . import views 
                                                    
app_name = 'youtube'                              
urlpatterns = [                                    
     path('youtube', views.get_youtube, name='youtube'),
     path('hidden_video/<int:pk>', views.hidden_video, name='hidden_video')
] 
