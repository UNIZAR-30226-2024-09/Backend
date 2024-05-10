from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from asgiref.sync import async_to_sync
from . import models
import json

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.user = self.scope['user']
        self.chat = get_object_or_404(models.Sala, pk=self.room_name)

        async_to_sync(self.channel_layer.group_add)(
            self.room_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name,
            self.channel_name
        )
    def chat_message(self, event):
        cuerpo = event['cuerpo']
        autor = event['autor']

        self.send(text_data=json.dumps({
            'cuerpo': cuerpo,
            'autor': autor
        }))
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        cuerpo = text_data_json['cuerpo']
        self.send(text_data=text_data)

        async_to_sync(self.channel_layer.group_send)(
            self.room_name,
            {
                'type': 'chat_message',
                'cuerpo': cuerpo,
                'autor': self.user.correo
            }
        )