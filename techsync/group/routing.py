from django.urls import path
from .consumers import *

websocket_urlpatterns = [
    path('ws/room/<str:chatroom_name>/', GrouproomConsumer.as_asgi()),
]