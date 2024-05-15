from ocpp.v16.call_result import DataTransferPayload

from .schema import DataTransferRequest, DataTransferResponse
from ocpp_service.configs import ACTIVE_CONNECTIONS
from ocpp_service.ocpp_controller import OCPP16Controller


async def data_transfer_handler(body: DataTransferRequest) -> DataTransferResponse:
    if body.charger_identify not in ACTIVE_CONNECTIONS:
        return DataTransferResponse(status='not_connected', data=None)

    connection: OCPP16Controller = ACTIVE_CONNECTIONS[body.charger_identify]

    result: DataTransferPayload = await connection.send_data_transfer_command(
        vendor_id=body.vendor_id,
        message_id=body.message_id,
        data=body.data
    )

    return DataTransferResponse(status=result.status.value, data=result.data)
