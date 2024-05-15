from ocpp.v16.call_result import SendLocalListPayload

from ocpp_service.configs import ACTIVE_CONNECTIONS
from ocpp_service.ocpp_controller import OCPP16Controller
from .schema import SendLocalListRequest, SendLocalListResponse


async def send_local_list_handler(body: SendLocalListRequest) -> SendLocalListResponse:
    if body.charger_identify not in ACTIVE_CONNECTIONS:
        return SendLocalListResponse(status='not_connected')

    connection: OCPP16Controller = ACTIVE_CONNECTIONS[body.charger_identify]

    result: SendLocalListPayload = await connection.send_local_list_command(
        list_version=body.list_version,
        local_authorization_list=body.local_authorization_list,
        update_type=body.update_type
    )

    return SendLocalListResponse(status=result.status.value)
