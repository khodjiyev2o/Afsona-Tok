from ocpp.v16.call_result import GetLocalListVersionPayload

from ocpp_service.configs import ACTIVE_CONNECTIONS
from ocpp_service.ocpp_controller import OCPP16Controller
from .schema import GetLocalListVersionRequest, GetLocalListVersionResponse


async def get_local_list_version_handler(body: GetLocalListVersionRequest) -> GetLocalListVersionResponse:
    if body.charger_identify not in ACTIVE_CONNECTIONS:
        return GetLocalListVersionResponse(status='not_connected')

    connection: OCPP16Controller = ACTIVE_CONNECTIONS[body.charger_identify]

    result: GetLocalListVersionPayload = await connection.send_get_local_version_command()

    return GetLocalListVersionResponse(status='applied', list_version=result.list_version)
