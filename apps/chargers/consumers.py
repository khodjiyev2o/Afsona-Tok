import json
from decimal import Decimal

from channels.generic.websocket import AsyncJsonWebsocketConsumer


class MobileJsonConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        if not self.scope['user'].is_authenticated:
            await self.close(code=4001, reason='User is not authenticated')

        await self.channel_layer.group_add('connectors', self.channel_name)
        user_direct_group = f"user_id_{self.scope['user'].id}"
        await self.channel_layer.group_add(user_direct_group, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('connectors', self.channel_name)
        await self.channel_layer.group_discard(f"user_id_{self.scope['user'].id}", self.channel_name)

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
        money: Decimal = event['money']
        battery_percent: int = event['battery_percent']
        consumed_khw: Decimal = event['consumed_kwh']
        transaction_id: int = event['transaction_id']
        status: str = event['status']

        data_json = json.dumps(
            {
                "type": "meter_values_data",
                "data": {
                    "transaction_id": int(transaction_id),
                    "money": str(money),
                    "battery_percent": battery_percent,
                    "consumed_kwh": consumed_khw,
                    "status": str(status)
                }
            }
        )

        await self.send(text_data=data_json)

    async def send_command_result(self, event):
        status = event['status']
        command_id = event['id']
        data_json = json.dumps({
            "type": 'command_result',
            "data": {
                "command_id": command_id,
                "status": status
            }
        })
        await self.send(text_data=data_json)
