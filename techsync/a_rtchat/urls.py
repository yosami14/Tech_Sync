from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_view, name='chat-home'),

    #private chat
    path('chat/<username>', views.get_or_create_chatroom, name='start-chat'),
    path('chat/room/<chatroom_name>', views.chat_view, name='chatroom'),
    path('chatrooms/', views.view_user_chatrooms, name='user-chatrooms'),
]