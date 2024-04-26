from ocpp_service.commands.cancel_reservation.schema import CancelReservationRequest, CancelReservationResponse
from ocpp_service.configs import ACTIVE_CONNECTIONS
from ocpp_service.ocpp_controller import OCPP16Controller


async def cancel_reservation_handler(body: CancelReservationRequest) -> CancelReservationResponse:
    if body.charger_identify not in ACTIVE_CONNECTIONS:
        return CancelReservationResponse(status=False)

    connection: OCPP16Controller = ACTIVE_CONNECTIONS[body.charger_identify]
    result = await connection.send_cancel_reservation_command(reservation_id=body.reservation_id)
    # todo add result to response
    return CancelReservationResponse(status=True)
