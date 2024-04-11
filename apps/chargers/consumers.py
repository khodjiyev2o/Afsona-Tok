import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer


class EchoConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('connectors', self.channel_name)
        await self.accept()
        print("Connected to WebSocket and added to 'connectors' group")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('connectors', self.channel_name)
        print("Disconnected from WebSocket and removed from 'connectors' group")

    async def connector_status(self, event):
        status = event['status']
        connector_id = event['connector_id']
        await self.send(
            text_data=json.dumps({
            'type': "connector":{
                'connector_id': connector_id
                'status': status
            }
        }))
