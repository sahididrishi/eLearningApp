# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class GlobalChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("WebSocket CONNECT attempt...")
        # Define a global room group name
        self.room_group_name = 'global_chat'
        # Add this channel to the group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        # Accept the WebSocket connection
        await self.accept()
        print("WebSocket CONNECT success!")

    async def disconnect(self, close_code):
        print("WebSocket disconnect with code:", close_code)
        # Remove this channel from the group on disconnect
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        print("Received message data:", text_data)
        data = json.loads(text_data)
        message = data.get('message', '')
        # Identify the sender (if authenticated)
        username = self.scope['user'].username if self.scope['user'].is_authenticated else "Anonymous"


        # Broadcast the message to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        # Send the broadcast message to the WebSocket client
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))