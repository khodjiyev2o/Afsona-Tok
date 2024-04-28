from ocpp_service.configs import ACTIVE_CONNECTIONS
from ocpp_service.ocpp_controller import OCPP16Controller
from .schema import RemoteStartRequest, RemoteStartResponse


async def clear_charging_profile_handler(body: RemoteStartRequest) -> RemoteStartResponse:
    if body.charger_identify not in ACTIVE_CONNECTIONS:
        return RemoteStartResponse(status=False)

    connection: OCPP16Controller = ACTIVE_CONNECTIONS[body.charger_identify]
    await connection.send_clear_charging_profile_command(
        charging_profile_id=body.charging_profile_id,
        connector_id=body.connector_id,
        charging_profile_purpose=body.charging_profile_purpose,
        stack_level=body.stack_level
    )

    return RemoteStartResponse(status=True)


