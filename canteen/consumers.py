"""
The one and only cosumer class.
"""


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

    async def report(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))
