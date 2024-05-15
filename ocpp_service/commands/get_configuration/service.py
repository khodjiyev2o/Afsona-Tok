from ocpp.v16.call_result import GetConfigurationPayload

from ocpp_service.configs import ACTIVE_CONNECTIONS
from ocpp_service.ocpp_controller import OCPP16Controller
from .schema import GetConfigurationRequest, GetConfigurationResponse


async def get_configuration_handler(body: GetConfigurationRequest) -> GetConfigurationResponse:
    if body.charger_identify not in ACTIVE_CONNECTIONS:
        return GetConfigurationResponse(status="not_connected")

    connection: OCPP16Controller = ACTIVE_CONNECTIONS[body.charger_identify]

    result: GetConfigurationPayload = await connection.send_get_configuration_command(keys=body.keys)

    return GetConfigurationResponse(
        status='applied',
        configuration_key=result.configuration_key,
        unknown_key=result.unknown_key
    )
