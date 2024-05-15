from fastapi import APIRouter, status

from .cancel_reservation import cancel_reservation_handler, CancelReservationResponse
from .change_availability import change_availability_handler, ChangeAvailabilityResponse
from .change_configuration import change_configuration_handler, ChangeConfigurationResponse
from .clear_cache import clear_cache_handler, ClearClearCacheResponse
from .clear_charging_profile import clear_charging_profile_handler, ClearChargingProfileResponse
from .data_transfer import data_transfer_handler, DataTransferResponse
from .get_composite_schedule import get_composite_schedule_handler, GetCompositeScheduleResponse
from .get_configuration import get_configuration_handler, GetConfigurationResponse
from .get_diagnostics import get_diagnostics_handler, GetDiagnosticsResponse
from .get_local_list_version import GetLocalListVersionResponse, get_local_list_version_handler
from .remote_start_transaction import remote_start_handler, RemoteStartResponse
from .remote_stop_transaction import remote_stop_handler, RemoteStopResponse
from .remote_stop_transaction import remote_stop_handler, RemoteStopResponse
from .reserve_now import reserve_now_handler, ReserveNowResponse
from .reset import reset_handler, ResetResponse
from .send_local_list import SendLocalListResponse, send_local_list_handler
from .set_charging_profile import SetChargingProfileResponse, set_charging_profile_handler
from .trigger_message import trigger_message_handler, TriggerMessageResponse
from .unlock_connector import unlock_connector_handler, UnlockConnectorResponse
from .update_firmware import update_firmware_handler, UpdateFirmwareResponse

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
    path='/clear_charging_profile/',
    endpoint=clear_charging_profile_handler,
    response_model=ClearChargingProfileResponse,
    status_code=status.HTTP_200_OK,
    methods=['POST'],
    description="Clear Charging Profile"
)

router.add_api_route(
    path='/data_transfer/',
    endpoint=data_transfer_handler,
    response_model=DataTransferResponse,
    status_code=status.HTTP_200_OK,
    methods=['POST'],
    description="Data Transfer"
)

router.add_api_route(
    path='/get_composite_schedule/',
    endpoint=get_composite_schedule_handler,
    response_model=GetCompositeScheduleResponse,
    status_code=status.HTTP_200_OK,
    methods=['POST'],
    description="Get Composite Schedule"
)

router.add_api_route(
    path='/get_configuration/',
    endpoint=get_configuration_handler,
    response_model=GetConfigurationResponse,
    status_code=status.HTTP_200_OK,
    methods=['POST'],
    description="Get Configuration"
)

router.add_api_route(
    path='/get_diagnostics/',
    endpoint=get_diagnostics_handler,
    response_model=GetDiagnosticsResponse,
    status_code=status.HTTP_200_OK,
    methods=['POST'],
    description="Get Diagnostics"
)

router.add_api_route(
    path='/get_local_list_version/',
    endpoint=get_local_list_version_handler,
    response_model=GetLocalListVersionResponse,
    status_code=status.HTTP_200_OK,
    methods=['POST'],
    description="Get Local List Version"
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

router.add_api_route(
    path='/reserve_now/',
    endpoint=reserve_now_handler,
    response_model=ReserveNowResponse,
    status_code=status.HTTP_200_OK,
    methods=['POST'],
    description="Reserve Now"
)

router.add_api_route(
    path='/reset/',
    endpoint=reset_handler,
    response_model=ResetResponse,
    status_code=status.HTTP_200_OK,
    methods=['POST'],
    description="Reset"
)

router.add_api_route(
    path='/trigger_message/',
    endpoint=trigger_message_handler,
    response_model=TriggerMessageResponse,
    status_code=status.HTTP_200_OK,
    methods=['POST'],
    description="Trigger Message"
)

router.add_api_route(
    path='/send_local_list/',
    endpoint=send_local_list_handler,
    response_model=SendLocalListResponse,
    status_code=status.HTTP_200_OK,
    methods=['POST'],
    description="Send Local List"
)

router.add_api_route(
    path='/set_charging_profile/',
    endpoint=set_charging_profile_handler,
    response_model=SetChargingProfileResponse,
    status_code=status.HTTP_200_OK,
    methods=['POST'],
    description="Set Charging Profile"
)

router.add_api_route(
    path='/unlock_connector/',
    endpoint=unlock_connector_handler,
    response_model=UnlockConnectorResponse,
    status_code=status.HTTP_200_OK,
    methods=['POST'],
    description="Unlock Connector"
)

router.add_api_route(
    path='/update_firmware/',
    endpoint=update_firmware_handler,
    response_model=UpdateFirmwareResponse,
    status_code=status.HTTP_200_OK,
    methods=['POST'],
    description="Update Firmware"
)
