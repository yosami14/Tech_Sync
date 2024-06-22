from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from asgiref.sync import async_to_sync
import json
from .models import *

class ChatroomConsumer(WebsocketConsumer):
    def connect(self): 
        self.user = self.scope['user']
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']
        self.chatroom = get_object_or_404(ChatGroup, group_name=self.chatroom_name)
        
        # Add the current channel to the chatroom group. 
        # This allows the channel to receive messages broadcast to the group(all user).
        async_to_sync(self.channel_layer.group_add)(
            self.chatroom_name,
            self.channel_name
        )

        # add and update online users (online users counter)
        if self.user not in self.chatroom.users_online.all():
            self.chatroom.users_online.add(self.user)
            self.update_online_count()

        self.accept()

    def disconnect(self, close_code):
        # Remove the current channel from the chatroom group.
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom_name,
            self.channel_name
        )
        # add and update online users (online users counter)
        if self.user in self.chatroom.users_online.all():
            self.chatroom.users_online.remove(self.user)
            self.update_online_count() 
# recive form
    def receive(self, text_data):
        #convert json to python dict
        text_data_json = json.loads(text_data)
        body = text_data_json['body']

        message = GroupMessage.objects.create(
            body = body,
            author = self.user,
            group = self.chatroom
        )

        event = {
            'type': 'message_handler',
            'message_id': message.id,
        }
        async_to_sync(self.channel_layer.group_send) (
            self.chatroom_name, event
        )


    def message_handler(self,event):
        message_id = event['message_id']
        message = GroupMessage.objects.get(id=message_id)
        context ={
            'message': message,
            'user': self.user,
        }
        html = render_to_string("a_rtchat/partial/chat_message_p.html",context)
        self.send(text_data=html)


    def update_online_count(self):
        online_count = self.chatroom.users_online.count() -1
        event = {
            'type': 'online_count_handler',
            'online_count': online_count,
        }
        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name,
            event
        )

    def online_count_handler(self,event):
        online_count = event['online_count']
        context = {
            'online_count': online_count,
        }
        html = render_to_string("a_rtchat/partial/online_count.html",context)
        self.send(text_data=html)