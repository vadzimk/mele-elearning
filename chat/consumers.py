import json

from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    """ accepts any websocket connection and
    echoes back to the client every message (no broadcasting) """
    def connect(self):
        """ invoked when new connection is received """
        self.accept()  # accepts any connection

    def disconnect(self, code):
        """ invoked when client disconnects """
        pass  # no action needed

    def receive(self, text_data=None, bytes_data=None):
        """ invoked when data are received """
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # send message to client
        self.send(text_data=json.dumps({'message': message}))
