from fastapi import APIRouter, status

from ocpp_service.commands.remote_start import remote_start_handler, RemoteStartResponse
from ocpp_service.commands.remote_stop import remote_stop_handler, RemoteStopResponse

router = APIRouter(prefix='/api/ocpp/commands')


router.add_api_route(
    path='/remote_start/',
    endpoint=remote_start_handler,
    response_model=RemoteStartResponse,
    status_code=status.HTTP_200_OK,
    methods=['POST']
)

router.add_api_route(
    path='/remote_stop/',
    endpoint=remote_stop_handler,
    response_model=RemoteStopResponse,
    status_code=status.HTTP_200_OK,
    methods=['POST']
)