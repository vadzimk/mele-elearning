import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.utils import timezone

class ChatConsumer(WebsocketConsumer):
    """ accepts any websocket connection and
    echoes back to the client every message (no broadcasting) """
    def connect(self):
        """ invoked when new connection is received """
        self.user = self.scope['user']
        self.id = self.scope['url_route']['kwargs']['course_id']
        self.room_group_name = f'chat_{self.id}'
        # join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()  # accepts this connection

    def disconnect(self, code):
        """ invoked when client disconnects """
        # leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        """ invoked when data are received """
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',  # corresponds to the name of the method that is invoked on consumers that receive the event
                'message': message,
                'user': self.user.username,
                'datetime': timezone.now().isoformat(),
            }
        )

    def chat_message(self, event):
        """ method name matches type key that is sent to the channel group
        when a message is received from the websocket """
        # send message to websocket
        self.send(text_data=json.dumps(event))