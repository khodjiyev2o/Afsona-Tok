from ocpp.v16.call_result import ChangeConfigurationPayload

from ocpp_service.configs import ACTIVE_CONNECTIONS
from ocpp_service.ocpp_controller import OCPP16Controller
from .schema import ChangeConfigurationRequest, ChangeConfigurationResponse


async def change_configuration_handler(body: ChangeConfigurationRequest) -> ChangeConfigurationResponse:
    if body.charger_identify not in ACTIVE_CONNECTIONS:
        return ChangeConfigurationResponse(status="not_connected")

    connection: OCPP16Controller = ACTIVE_CONNECTIONS[body.charger_identify]

    result: ChangeConfigurationPayload = await connection.send_change_configuration_command(
        key=body.key, value=body.value
    )

    return ChangeConfigurationResponse(status=result.status)
