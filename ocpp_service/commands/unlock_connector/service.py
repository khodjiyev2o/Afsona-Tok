from ocpp.v16.call_result import UnlockConnectorPayload

from ocpp_service.configs import ACTIVE_CONNECTIONS
from ocpp_service.ocpp_controller import OCPP16Controller
from .schema import UnlockConnectorRequest, UnlockConnectorResponse


async def unlock_connector_handler(body: UnlockConnectorRequest) -> UnlockConnectorResponse:
    if body.charger_identify not in ACTIVE_CONNECTIONS:
        return UnlockConnectorResponse(status="not_connected")

    connection: OCPP16Controller = ACTIVE_CONNECTIONS[body.charger_identify]

    result: UnlockConnectorPayload = await connection.send_unlock_connector_command(
        connector_id=body.connector_id
    )

    return UnlockConnectorResponse(status=result.status)
