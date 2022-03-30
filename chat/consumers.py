import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from models import Message, User


class ChatConsumer(AsyncWebsocketConsumer):
    def fetch_messages(self, data):
        messages = Message.last_10_massages()
        content = {
            'messages': self.messages_to_json(messages)
        }

    def new_mesage(self, data):
        user_message = data['from']
        user = User.objects.filter(username=user_message)[0]
        message = Message.objects.create(user=user, content=data['message'])
        content = {
            'command': 'new_message',
            'message':self.messages_to_json(message)
        }
        return self.send_chat_message(content)


    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.messages_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            'user': message.user.username,
            'room': message.room.title,
            'timestamp': message.timestamp,
            'content': str(message.content),
        }

    commands = {
        'fetch_messages': fetch_messages,
        'new_mesage': new_mesage
    }

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(
            self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))
