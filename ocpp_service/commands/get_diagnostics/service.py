from ocpp.v16.call_result import GetDiagnosticsPayload

from ocpp_service.configs import ACTIVE_CONNECTIONS
from ocpp_service.ocpp_controller import OCPP16Controller
from .schema import GetDiagnosticsRequest, GetDiagnosticsResponse


async def get_diagnostics_handler(body: GetDiagnosticsRequest) -> GetDiagnosticsResponse:
    if body.charger_identify not in ACTIVE_CONNECTIONS:
        return GetDiagnosticsResponse(status='not_connected')

    connection: OCPP16Controller = ACTIVE_CONNECTIONS[body.charger_identify]

    result: GetDiagnosticsPayload = await connection.send_get_diagnostics_command(
        location=body.location,
        retries=body.retries,
        retry_interval=body.retry_interval,
        start_time=body.start_time,
        stop_time=body.stop_time
    )

    return GetDiagnosticsResponse(status='applied', file_name=result.file_name)
