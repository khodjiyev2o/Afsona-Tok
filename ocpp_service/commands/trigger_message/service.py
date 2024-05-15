from ocpp.v16.call_result import TriggerMessagePayload

from ocpp_service.configs import ACTIVE_CONNECTIONS
from ocpp_service.ocpp_controller import OCPP16Controller
from .schema import TriggerMessageRequest, TriggerMessageResponse


async def trigger_message_handler(body: TriggerMessageRequest) -> TriggerMessageResponse:
    if body.charger_identify not in ACTIVE_CONNECTIONS:
        return TriggerMessageResponse(status="not_connected")

    connection: OCPP16Controller = ACTIVE_CONNECTIONS[body.charger_identify]

    result: TriggerMessagePayload = await connection.send_trigger_message_command(
        requested_message=body.trigger_message,
        connector_id=body.connector_id,
    )

    return TriggerMessageResponse(status=result.status)
