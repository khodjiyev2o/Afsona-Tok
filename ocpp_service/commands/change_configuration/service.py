from .schema import ChangeConfigurationRequest, ChangeConfigurationResponse
from ocpp_service.configs import ACTIVE_CONNECTIONS
from ocpp_service.ocpp_controller import OCPP16Controller


async def change_configuration_handler(body: ChangeConfigurationRequest) -> ChangeConfigurationResponse:
    if body.charger_identify not in ACTIVE_CONNECTIONS:
        return ChangeConfigurationResponse(status=False)

    connection: OCPP16Controller = ACTIVE_CONNECTIONS[body.charger_identify]

    await connection.send_change_configuration_command(key=body.key, value=body.value)

    return ChangeConfigurationResponse(status=True)
