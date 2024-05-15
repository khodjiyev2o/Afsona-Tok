from ocpp.v16.call_result import ResetPayload

from ocpp_service.configs import ACTIVE_CONNECTIONS
from ocpp_service.ocpp_controller import OCPP16Controller
from .schema import ResetRequest, ResetResponse


async def reset_handler(body: ResetRequest) -> ResetResponse:
    if body.charger_identify not in ACTIVE_CONNECTIONS:
        return ResetResponse(status="not_connected")

    connection: OCPP16Controller = ACTIVE_CONNECTIONS[body.charger_identify]

    result: ResetPayload = await connection.send_reset_command(
        reset_type=body.reset_type
    )

    return ResetResponse(status=result.status)
