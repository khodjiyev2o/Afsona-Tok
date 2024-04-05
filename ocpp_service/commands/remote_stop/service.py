from ocpp.v16.enums import RemoteStartStopStatus

from ocpp_service.commands.remote_stop.schema import RemoteStopRequest, RemoteStopResponse
from ocpp_service.configs import ACTIVE_CONNECTIONS
from ocpp_service.ocpp_controller import OCPP16Controller


async def remote_stop_handler(body: RemoteStopRequest) -> RemoteStopRequest:
    if body.charger_identify not in ACTIVE_CONNECTIONS:
        return RemoteStopRequest(status=False)

    connection: OCPP16Controller = ACTIVE_CONNECTIONS[body.charger_identify]
    response = await connection.send_remote_stop_transaction_command(transaction_id=body.transaction_id)

    return RemoteStopRequest(status=response.status == RemoteStartStopStatus.accepted)
