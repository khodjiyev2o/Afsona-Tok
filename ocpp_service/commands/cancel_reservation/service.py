from ocpp.v16.call_result import CancelReservationPayload

from ocpp_service.configs import ACTIVE_CONNECTIONS
from ocpp_service.ocpp_controller import OCPP16Controller
from .schema import CancelReservationRequest, CancelReservationResponse


async def cancel_reservation_handler(body: CancelReservationRequest) -> CancelReservationResponse:
    if body.charger_identify not in ACTIVE_CONNECTIONS:
        return CancelReservationResponse(status='not_connected')

    connection: OCPP16Controller = ACTIVE_CONNECTIONS[body.charger_identify]

    result: CancelReservationPayload = await connection.send_cancel_reservation_command(
        reservation_id=body.reservation_id
    )
    return CancelReservationResponse(status=result.status)
