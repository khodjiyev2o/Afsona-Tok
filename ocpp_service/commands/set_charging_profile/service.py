from ocpp.v16.call_result import SetChargingProfilePayload

from ocpp_service.configs import ACTIVE_CONNECTIONS
from ocpp_service.ocpp_controller import OCPP16Controller
from .schema import SetChargingProfileRequest, SetChargingProfileResponse


async def set_charging_profile_handler(body: SetChargingProfileRequest) -> SetChargingProfileResponse:
    if body.charger_identify not in ACTIVE_CONNECTIONS:
        return SetChargingProfileResponse(status='not_connected')

    connection: OCPP16Controller = ACTIVE_CONNECTIONS[body.charger_identify]

    result: SetChargingProfilePayload = await connection.send_set_charging_profile_command(
        connector_id=body.connector_id,
        cs_charging_profiles=body.cs_charging_profiles
    )

    return SetChargingProfileResponse(status=result.status.value)
