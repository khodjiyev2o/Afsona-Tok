from fastapi import FastAPI
from starlette.websockets import WebSocket, WebSocketDisconnect

from ocpp_service.commands import router
from ocpp_service.utils import manager

app = FastAPI(title="OCPP Controller Websocket Service")

app.include_router(router)


@app.websocket("/ocpp/ws/{charger_identify}")
async def websocket_endpoint(websocket: WebSocket, charge_point_identify: str):
    try:
        await manager.connect(websocket, charge_point_identify)
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        await manager.disconnect(charge_point_identify)
