import aiohttp
from fastapi import BackgroundTasks
from ocpp.v16.enums import RemoteStartStopStatus

from ocpp_service.commands.remote_stop.schema import RemoteStopRequest, RemoteStopResponse
from ocpp_service.configs import ACTIVE_CONNECTIONS, WEBSOCKET_COMMAND_CALLBACK_URL
from ocpp_service.ocpp_controller import OCPP16Controller


async def remote_stop_handler(body: RemoteStopRequest, background_tasks: BackgroundTasks) -> RemoteStopResponse:
    if body.charger_identify not in ACTIVE_CONNECTIONS:
        return RemoteStopResponse(status=False)

    connection: OCPP16Controller = ACTIVE_CONNECTIONS[body.charger_identify]
    background_tasks.add_task(send_command_to_charger, connection=connection, body=body)

    return RemoteStopResponse(status=True)


async def send_command_to_charger(connection: OCPP16Controller, body: RemoteStopRequest):
    response = await connection.send_remote_stop_transaction_command(
        transaction_id=body.transaction_id
    )
    async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=2), headers={"Content-Type": "application/json"}
    ) as session:
        async with session.post(
                url=WEBSOCKET_COMMAND_CALLBACK_URL.format(body.id_tag),
                json={"status": response.status == RemoteStartStopStatus.accepted}
        ) as response:
            await response.json()
