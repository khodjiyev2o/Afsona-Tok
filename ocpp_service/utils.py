import aiohttp
from starlette.websockets import WebSocket

from ocpp_service.configs import ACTIVE_CONNECTIONS, WEBSOCKET_DISCONNECT_CALLBACK_URL
from ocpp_service.ocpp_controller import OCPP16Controller


class SocketAdapter:
    def __init__(self, websocket: WebSocket):
        self._ws = websocket

    async def recv(self) -> str:
        return await self._ws.receive_text()

    async def send(self, msg) -> None:
        await self._ws.send_text(msg)


class ConnectionManager:
    async def connect(self, websocket: WebSocket, charger_identify: str):
        await websocket.accept(subprotocol='ocpp1.6')
        connection = OCPP16Controller(charger_identify, SocketAdapter(websocket))
        ACTIVE_CONNECTIONS[connection.id] = connection
        await connection.start()

    async def disconnect(self, charger_identify: str, reason: str) -> None:
        del ACTIVE_CONNECTIONS[charger_identify]
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    url=WEBSOCKET_DISCONNECT_CALLBACK_URL.format(charger_identify),
                    json={'reason': reason}
            ) as response:
                await response.json()


manager = ConnectionManager()


