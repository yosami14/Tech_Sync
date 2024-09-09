from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.dashboard, name='conference'),
    path('meeting', views.videocall, name='meeting'),
    path('join_room', views.join_room, name='join-room'),
]