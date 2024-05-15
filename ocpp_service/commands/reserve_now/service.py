from ocpp.v16.call_result import ReserveNowPayload

from .schema import ReserveNowRequest, ReserveNowResponse
from ocpp_service.configs import ACTIVE_CONNECTIONS
from ocpp_service.ocpp_controller import OCPP16Controller


async def reserve_now_handler(body: ReserveNowRequest) -> ReserveNowResponse:
    if body.charger_identify not in ACTIVE_CONNECTIONS:
        return ReserveNowResponse(status='not_connected')

    connection: OCPP16Controller = ACTIVE_CONNECTIONS[body.charger_identify]

    result: ReserveNowPayload = await connection.send_reverse_now_command(
        connector_id=body.connector_id,
        expiry_date=body.expiry_date,
        id_tag=body.id_tag,
        reservation_id=body.reservation_id
    )

    return ReserveNowResponse(status=result.status)
