from fastapi import APIRouter, status

from .remote_start_transaction import remote_start_handler, RemoteStartResponse
from .remote_stop_transaction import remote_stop_handler, RemoteStopResponse
from .remote_stop_transaction import remote_stop_handler, RemoteStopResponse
from .change_availability import change_availability_handler, ChangeAvailabilityResponse
from .change_configuration import change_configuration_handler, ChangeConfigurationResponse
from .cancel_reservation import cancel_reservation_handler, CancelReservationResponse
from .clear_cache import clear_cache_handler, ClearClearCacheResponse

router = APIRouter(prefix='/ocpp/http/commands')

router.add_api_route(
    path="/cancel_reservation/",
    endpoint=cancel_reservation_handler,
    response_model=CancelReservationResponse,
    status_code=status.HTTP_200_OK,
    methods=['POST'],
    description="Cancel Reservation"
)

router.add_api_route(
    path="/change_availability/",
    endpoint=change_availability_handler,
    response_model=ChangeAvailabilityResponse,
    status_code=status.HTTP_200_OK,
    methods=['POST'],
    description="Change availability"
)

router.add_api_route(
    path="/change_configuration/",
    endpoint=change_configuration_handler,
    response_model=ChangeConfigurationResponse,
    status_code=status.HTTP_200_OK,
    methods=['POST'],
    description="Change configuration"
)

router.add_api_route(
    path="/clear_cache/",
    endpoint=clear_cache_handler,
    response_model=ClearClearCacheResponse,
    status_code=status.HTTP_200_OK,
    methods=['POST'],
    description="Clear cache"
)

router.add_api_route(
    path='/remote_start/',
    endpoint=remote_start_handler,
    response_model=RemoteStartResponse,
    status_code=status.HTTP_200_OK,
    methods=['POST'],
    description="Remote start Transaction"
)

router.add_api_route(
    path='/remote_stop/',
    endpoint=remote_stop_handler,
    response_model=RemoteStopResponse,
    status_code=status.HTTP_200_OK,
    methods=['POST'],
    description="Remote Stop Transaction"
)

