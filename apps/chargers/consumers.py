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

    async def send_connector_status(self, event):
        status = event['status']
        connector_id = event['connector_id']
        data = {
            "type": 'connector',
            "data": {
                "connector_id": connector_id,
                "status": status
            }
        }
        await self.send(text_data=json.dumps(data))

    async def send_transaction_data(self, event):
        money = event['money']
        battery_percent = event['battery_percent']
        consumed_khw = event['consumed_kwh']

        transaction_id = event['transaction_id']
        await self.send(
            text_data=json.dumps({
                'type': "transaction",
                "data": {
                    "transaction_id": transaction_id,
                    "money": money,
                    "battery_percent": battery_percent,
                    "consumed_kwh": consumed_khw
                }
            }))
