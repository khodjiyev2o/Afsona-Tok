from ocpp.v16.call_result import ClearCachePayload

from ocpp_service.configs import ACTIVE_CONNECTIONS
from ocpp_service.ocpp_controller import OCPP16Controller
from .schema import ClearClearCacheRequest, ClearClearCacheResponse


async def clear_cache_handler(body: ClearClearCacheRequest) -> ClearClearCacheResponse:
    if body.charger_identify not in ACTIVE_CONNECTIONS:
        return ClearClearCacheResponse(status="not_connected")

    connection: OCPP16Controller = ACTIVE_CONNECTIONS[body.charger_identify]

    result: ClearCachePayload = await connection.send_clear_cache_command()

    return ClearClearCacheResponse(status=result.status.value)
