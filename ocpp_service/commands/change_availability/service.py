from ocpp.v16.call_result import ChangeAvailabilityPayload

from ocpp_service.configs import ACTIVE_CONNECTIONS
from ocpp_service.ocpp_controller import OCPP16Controller
from .schema import ChangeAvailabilityRequest, ChangeAvailabilityResponse


async def change_availability_handler(body: ChangeAvailabilityRequest) -> ChangeAvailabilityResponse:
    if body.charger_identify not in ACTIVE_CONNECTIONS:
        return ChangeAvailabilityResponse(status='Not connected')

    connection: OCPP16Controller = ACTIVE_CONNECTIONS[body.charger_identify]

    result: ChangeAvailabilityPayload = await connection.send_change_change_availability_command(
        connector_id=body.connector_id,
        availability_type=body.availability_type
    )

    return ChangeAvailabilityResponse(status=result.status)
