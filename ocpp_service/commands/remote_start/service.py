from ocpp.v16.enums import RemoteStartStopStatus

from ocpp_service.commands.remote_start.schema import RemoteStartRequest, RemoteStartResponse
from ocpp_service.configs import ACTIVE_CONNECTIONS
from ocpp_service.ocpp_controller import OCPP16Controller


async def remote_start_handler(body: RemoteStartRequest) -> RemoteStartResponse:
    if body.charger_identify not in ACTIVE_CONNECTIONS:
        return RemoteStartResponse(status=False)

    connection: OCPP16Controller = ACTIVE_CONNECTIONS[body.charger_identify]
    response = await connection.send_remote_start_transaction_command(
        connector_id=body.connector_id, id_tag=body.id_tag
    )

    return RemoteStartResponse(status=response.status == RemoteStartStopStatus.accepted)
