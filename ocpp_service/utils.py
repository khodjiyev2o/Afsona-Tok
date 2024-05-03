import aiohttp
import sentry_sdk
from starlette.websockets import WebSocket

from ocpp_service.configs import ACTIVE_CONNECTIONS, WEBSOCKET_DISCONNECT_CALLBACK_URL
from ocpp_service.ocpp_controller import OCPP16Controller


async def send_raw_messages_to_telegram_channel(charger_id: str, message: str, sms_type: str = 'in'):
    channel_credentials: dict = {
        'in': {
            'token': '6776606012:AAHG0sKQtsfJ-PjDnNhRyw3QDr3mtRPQlM0',
            'chat_id': '-1002009651619'
        },
        'out': {
            'token': '6776606012:AAHG0sKQtsfJ-PjDnNhRyw3QDr3mtRPQlM0',
            'chat_id': '-1002000950555'
        }
    }

    url = f'https://api.telegram.org/bot{channel_credentials[sms_type]["token"]}/sendMessage'
    params = {
        'chat_id': channel_credentials[sms_type]["chat_id"],
        'text': f'{charger_id}\n{message}'
    }
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=1)) as session:
            async with session.get(url, params=params):
                ...
    except Exception as ex:
        sentry_sdk.capture_exception(ex)


class SocketAdapterAndLogger:
    def __init__(self, websocket: WebSocket):
        self._ws = websocket

    async def recv(self) -> str:
        received_message = await self._ws.receive_text()
        await send_raw_messages_to_telegram_channel(
            charger_id=self._ws.path_params.get('charger_identify', 'unknown'),
            message=received_message
        )
        return received_message

    async def send(self, msg) -> None:
        await self._ws.send_text(msg)
        await send_raw_messages_to_telegram_channel(
            charger_id=self._ws.path_params.get('charger_identify', 'unknown'),
            message=msg, sms_type='out'
        )


class ConnectionManager:
    async def connect(self, websocket: WebSocket, charger_identify: str):
        await websocket.accept(subprotocol='ocpp1.6')
        connection = OCPP16Controller(charger_identify, SocketAdapterAndLogger(websocket))
        ACTIVE_CONNECTIONS[connection.id] = connection
        await send_raw_messages_to_telegram_channel(
            charger_id=connection.id,
            message="set : " + str((ACTIVE_CONNECTIONS, id(ACTIVE_CONNECTIONS))),
            sms_type='out'
        )
        await connection.start()

    async def disconnect(self, charger_identify: str, reason: str) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    url=WEBSOCKET_DISCONNECT_CALLBACK_URL.format(charger_identify),
                    json={'reason': reason}
            ) as response:
                await response.json()


manager = ConnectionManager()
