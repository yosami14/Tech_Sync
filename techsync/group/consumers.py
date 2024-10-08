from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from .models import *
import json
from django.template.loader import render_to_string
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class GrouproomConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']
        self.room = get_object_or_404(Room, id=self.chatroom_name)

        

        # Add the user to a group specific to the chat room
        self.room_group_name = f'chat_{self.chatroom_name}'
        async_to_sync(get_channel_layer().group_add)(
            self.room_group_name,
            self.channel_name
        )
        # online users count
        if self.user not in self.room.users_online.all():
            self.room.users_online.add(self.user)
            self.update_online_count()

        self.accept()

    def disconnect(self, close_code):
        # Remove the user from the group when they disconnect
        async_to_sync(get_channel_layer().group_discard)(
            self.room_group_name,
            self.channel_name
        )
        # online users count
        if self.user in self.room.users_online.all():
            self.room.users_online.remove(self.user)
            self.update_online_count()
            
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body = text_data_json['body']

        message = Message.objects.create(
            body=body,
            user=self.user,
            room=self.room,
        )
        context = {
            'message': message,
            'user': self.user,
        }
        html = render_to_string("group/partial/room_messages_p.html", context)

        # Send the message to all users in the group
        async_to_sync(get_channel_layer().group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': html
            }
        )

    # This method will be called when a 'chat_message' event is sent to the group
    def chat_message(self, event):
        message = event['message']

        # Send the message to the WebSocket
        self.send(text_data=message)

    # handler for online users
    def update_online_count(self):
        online_count = self.room.users_online.count() 
        event = {
            'type': 'online_count_handler',
            'online_count': online_count,
        }
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            event
        )

    def online_count_handler(self,event):
        online_count = event['online_count']
        context = {
            'online_count': online_count,
            'chat_group': self.room,
            'participants': self.room.participants.all(),
        }

        html = render_to_string("group/partial/online_count.html",context)
        self.send(text_data=html)