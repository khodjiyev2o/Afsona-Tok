from ocpp.v16.call_result import ClearChargingProfilePayload

from ocpp_service.configs import ACTIVE_CONNECTIONS
from ocpp_service.ocpp_controller import OCPP16Controller
from .schema import ClearChargingProfileRequest, ClearChargingProfileResponse


async def clear_charging_profile_handler(body: ClearChargingProfileRequest) -> ClearChargingProfileResponse:
    if body.charger_identify not in ACTIVE_CONNECTIONS:
        return ClearChargingProfileResponse(status='not_connected')

    connection: OCPP16Controller = ACTIVE_CONNECTIONS[body.charger_identify]

    result: ClearChargingProfilePayload = await connection.send_clear_charging_profile_command(
        charging_profile_id=body.charger_profile_id,
        connector_id=body.connector_id,
        charging_profile_purpose=body.charging_profile_purpose,
        stack_level=body.stack_level
    )

    return ClearChargingProfileResponse(status=result.status)
