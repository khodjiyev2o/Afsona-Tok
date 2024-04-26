from .schema import ClearClearCacheRequest, ClearClearCacheResponse
from ocpp_service.configs import ACTIVE_CONNECTIONS
from ocpp_service.ocpp_controller import OCPP16Controller


async def clear_cache_handler(body: ClearClearCacheRequest) -> ClearClearCacheResponse:
    if body.charger_identify not in ACTIVE_CONNECTIONS:
        return ClearClearCacheResponse(status=False)

    connection: OCPP16Controller = ACTIVE_CONNECTIONS[body.charger_identify]

    await connection.send_clear_cache_command()

    return ClearClearCacheResponse(status=True)
