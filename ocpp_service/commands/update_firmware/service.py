from ocpp_service.configs import ACTIVE_CONNECTIONS
from ocpp_service.ocpp_controller import OCPP16Controller
from .schema import UpdateFirmwareRequest, UpdateFirmwareResponse


async def update_firmware_handler(body: UpdateFirmwareRequest) -> UpdateFirmwareResponse:
    if body.charger_identify not in ACTIVE_CONNECTIONS:
        return UpdateFirmwareResponse(status="not_connected")

    connection: OCPP16Controller = ACTIVE_CONNECTIONS[body.charger_identify]

    await connection.send_update_firmware_command(
        location=body.location,
        retries=body.retries,
        retrieve_date=body.retrieve_date,
        retry_interval=body.retry_interval
    )

    return UpdateFirmwareResponse(status="Applied")
