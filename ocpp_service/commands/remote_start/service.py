import asyncio

import aiohttp
from fastapi import BackgroundTasks
from ocpp.v16.enums import RemoteStartStopStatus

from ocpp_service.commands.remote_start.schema import RemoteStartRequest, RemoteStartResponse
from ocpp_service.configs import ACTIVE_CONNECTIONS, WEBSOCKET_COMMAND_CALLBACK_URL
from ocpp_service.ocpp_controller import OCPP16Controller


async def remote_start_handler(body: RemoteStartRequest, background_tasks: BackgroundTasks) -> RemoteStartResponse:
    if body.charger_identify not in ACTIVE_CONNECTIONS:
        return RemoteStartResponse(status=False)

    connection: OCPP16Controller = ACTIVE_CONNECTIONS[body.charger_identify]
    background_tasks.add_task(send_command_to_charger, connection=connection, body=body)

    return RemoteStartResponse(status=True)


async def send_command_to_charger(connection: OCPP16Controller, body: RemoteStartRequest):
    await asyncio.sleep(2)
    response = await connection.send_remote_start_transaction_command(
        connector_id=body.connector_id, id_tag=body.id_tag
    )
    async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=2), headers={"Content-Type": "application/json"}
    ) as session:
        async with session.post(
                url=WEBSOCKET_COMMAND_CALLBACK_URL.format(body.id_tag),
                json={"status": response.status == RemoteStartStopStatus.accepted}
        ) as response:
            await response.json()
