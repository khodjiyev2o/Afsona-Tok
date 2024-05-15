from ocpp.v16.call_result import GetCompositeSchedulePayload

from ocpp_service.configs import ACTIVE_CONNECTIONS
from ocpp_service.ocpp_controller import OCPP16Controller
from .schema import GetCompositeScheduleRequest, GetCompositeScheduleResponse


async def get_composite_schedule_handler(body: GetCompositeScheduleRequest) -> GetCompositeScheduleResponse:
    if body.charger_identify not in ACTIVE_CONNECTIONS:
        return GetCompositeScheduleResponse(status='not_connected')

    connection: OCPP16Controller = ACTIVE_CONNECTIONS[body.charger_identify]

    result: GetCompositeSchedulePayload = await connection.send_get_composite_schedule_command(
        connector_id=body.connector_id,
        duration=body.duration,
        charging_rate_unit=body.charging_rate_unit
    )

    return GetCompositeScheduleResponse(
        status=result.status.value,
        connector_id=result.connector_id,
        schedule_start=result.schedule_start,
        charging_schedule=result.charging_schedule
    )
