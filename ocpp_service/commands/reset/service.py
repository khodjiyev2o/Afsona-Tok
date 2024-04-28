from ocpp_service.commands.reset.schema import ResetRequest, ResetResponse
from ocpp_service.configs import ACTIVE_CONNECTIONS
from ocpp_service.ocpp_controller import OCPP16Controller


async def reset_handler(body: ResetRequest) -> ResetResponse:
    if body.charger_identify not in ACTIVE_CONNECTIONS:
        return ResetResponse(status=False)

    connection: OCPP16Controller = ACTIVE_CONNECTIONS[body.charger_identify]

    response = await connection.send_reset_command(reset_type=body.reset_type) # noqa
    return ResetResponse(status=True)
