from channels.generic.websocket import AsyncWebsocketConsumer
import json


class ReportConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'report'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):

        # Send message
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'message',
                'message': ''
            }
        )

    # Receive message from group
    async def message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': ''
        }))
