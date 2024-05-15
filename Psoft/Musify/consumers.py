from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from asgiref.sync import async_to_sync
from . import models
import json

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.user = self.scope['user']
        print(self.user)
        self.chat = get_object_or_404(models.Sala, pk=self.room_name)

        # Add the consumer to the group for the specific chat room
        async_to_sync(self.channel_layer.group_add)(
            self.room_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Remove the consumer from the group when disconnecting
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name,
            self.channel_name
        )

    def chat_message(self, event):
        # Send a chat message to the client
        cuerpo = event['cuerpo']
        autor = event['autor']
        self.send(text_data=json.dumps({
            'cuerpo': cuerpo,
            'autor': autor
        }))

    def receive(self, text_data):
        # Receive a message from the client and broadcast it to the group
        text_data_json = json.loads(text_data)
        cuerpo = text_data_json.get('cuerpo', '')
        
        # Check if the user is authenticated
        if self.user.is_authenticated:
            autor = self.user.correo
        else:
            autor = 'Anonymous'
        
        if cuerpo.strip():
            async_to_sync(self.channel_layer.group_send)(
                self.room_name,
                {
                    'type': 'chat_message',
                    'cuerpo': cuerpo,
                    'autor': autor
                }
            )

