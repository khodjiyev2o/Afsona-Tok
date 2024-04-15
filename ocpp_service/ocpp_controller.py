from __future__ import annotations

from datetime import datetime

import aiohttp
from ocpp.routing import on
from ocpp.v16 import ChargePoint
from ocpp.v16 import call
from ocpp.v16.datatypes import IdTagInfo
from ocpp.v16.enums import (
    Action, AuthorizationStatus, RegistrationStatus,
    CancelReservationStatus, AvailabilityStatus,
    ConfigurationStatus, ClearCacheStatus, DataTransferStatus,
    GetCompositeScheduleStatus, ReservationStatus,
    ResetStatus, TriggerMessageStatus, UnlockStatus,
    AvailabilityType, ChargingProfilePurposeType, ChargingRateUnitType,
    ResetType, UpdateType, MessageTrigger, RemoteStartStopStatus
)

from ocpp_service.configs import OCPP_RAW_MESSAGES_SERVICE_URL


async def send_raw_messages_to_telegram_channel(message):
    token = '6776606012:AAHG0sKQtsfJ-PjDnNhRyw3QDr3mtRPQlM0'
    channel_id = -1002009651619

    url = f'https://api.telegram.org/bot{token}/sendMessage'
    params = {
        'chat_id': channel_id,
        'text': message
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            await response.json()


class OCPP16Controller(ChargePoint):

    async def route_message(self, raw_msg):
        # await send_raw_messages_to_telegram_channel(f"{self.id}/\n{raw_msg}")
        return await super().route_message(raw_msg)

    @on(action=Action.Authorize)
    async def on_authorize(self, **kwargs):
        """
            Handle the authorization request.

            This method is invoked when 'authorization' request is received.

            :param kwargs: Additional keyword arguments passed to the method:
                   - id_tag: str: The ID tag associated with the authorization request.

            :return: An instance of AuthorizePayload containing authorization information.
        """
        data = await self.__send_request(sms_type='authorize', data=kwargs)
        data = data.get('id_tag_info', {})
        payload = self._call_result.AuthorizePayload(
            id_tag_info=IdTagInfo(
                status=data.get('status', AuthorizationStatus.invalid),
                parent_id_tag=data.get('parent_id_tag', None),
                expiry_date=data.get('expiry_date', None)
            )
        )
        return payload

    @on(action=Action.BootNotification)
    async def on_boot_notification(self, **kwargs):
        """
            Handle boot notification request.

            This method is invoked when a 'boot notification' request is received.

            :param kwargs: Additional keyword arguments passed to the method.
                   - charge_box_serial_number: Optional[str] - Serial number of the Charge Box inside the Charge Point.
                   - charge_point_model: str - Model of the Charge Point (required).
                   - charge_point_serial_number: Optional[str] - Serial number of the Charge Point.
                   - charge_point_vendor: str - Vendor of the Charge Point (required).
                   - firmware_version: Optional[str] - Firmware version of the Charge Point.
                   - iccid: Optional[str] - ICCID of the modem’s SIM card.
                   - imsi: Optional[str] - IMSI of the modem’s SIM card.
                   - meter_serial_number: Optional[str] - Serial number of the main power meter of the Charge Point.
                   - meter_type: Optional[str] - Type of the main power meter of the Charge Point.

            :return: An instance of BootNotificationPayload containing the response to the boot notification.
        """

        response = await self.__send_request(sms_type='boot_notification', data=kwargs)

        payload = self._call_result.BootNotificationPayload(
            current_time=datetime.utcnow().isoformat(),
            interval=response.get("interval", 10),
            status=response.get("status", RegistrationStatus.rejected)
        )
        return payload

    @on(action=Action.CancelReservation)
    async def on_cancel_reservation(self, **kwargs):
        response = await self.__send_request(sms_type='cancel_reservation', data=kwargs)
        payload = self._call_result.CancelReservationPayload(
            status=response.get('status', CancelReservationStatus.rejected)
        )
        return payload

    @on(action=Action.ChangeConfiguration)
    async def on_change_availability(self, **kwargs):
        response = await self.__send_request(sms_type='change_availability', data=kwargs)
        return self._call_result.ChangeAvailabilityPayload(status=response.get("status", AvailabilityStatus.rejected))

    @on(action=Action.ChangeConfiguration)
    async def on_change_configuration(self, **kwargs):
        response = await self.__send_request(sms_type='change_configuration', data=kwargs)
        return self._call_result.ChangeConfigurationPayload(
            status=response.get("status", ConfigurationStatus.not_supported))

    @on(action=Action.ClearCache)
    async def on_clear_cache(self, **kwargs):
        response = await self.__send_request(sms_type='clear_cache', data=kwargs)
        await self._call_result.ClearCachePayload(status=response.get('status', ClearCacheStatus.rejected))

    @on(action=Action.DataTransfer)
    async def on_data_transfer(self, **kwargs):
        response = await self.__send_request(sms_type='data_transfer', data=kwargs)
        await self._call_result.DataTransferPayload(
            status=response.get('status', DataTransferStatus.rejected),
            data=response.get('data', None)
        )

    @on(action=Action.DiagnosticsStatusNotification)
    async def on_diagnostics_status_notification(self, **kwargs):
        await self.__send_request(
            sms_type='diagnostics_status_notification', data=kwargs
        )  # there is no arg from response
        return self._call_result.DiagnosticsStatusNotificationPayload()

    @on(action=Action.FirmwareStatusNotification)
    async def on_firmware_status_notification(self, **kwargs):
        await self.__send_request(sms_type='firmware_status_notification', data=kwargs)  # there is no arg from response
        return self._call_result.FirmwareStatusNotificationPayload()

    @on(action=Action.GetCompositeSchedule)
    async def on_get_composite_schedule(self, **kwargs):
        response = await self.__send_request(sms_type='get_composite_schedule', data=kwargs)
        return self._call_result.GetCompositeSchedulePayload(
            status=response.get("status", GetCompositeScheduleStatus.rejected),
            connector_id=response.get('connector_id', None),
            schedule_start=response.get('schedule_start', None),
            charging_schedule=response.get('charging_schedule', None)
        )

    @on(action=Action.GetConfiguration)
    async def on_get_configuration(self, **kwargs):
        response = await self.__send_request(sms_type='get_configuration', data=kwargs)
        return self._call_result.GetConfigurationPayload(
            configuration_key=response.get('configuration_key', None),
            unknown_key=response.get('unknown_key', None)
        )

    @on(action=Action.GetDiagnostics)
    async def on_get_diagnostics(self, **kwargs):
        response = await self.__send_request(sms_type='get_diagnostics', data=kwargs)
        return self._call_result.GetDiagnosticsPayload(file_name=response.get('file_name', None))

    @on(action=Action.GetLocalListVersion)
    async def on_get_local_list_version(self, **kwargs):
        response = await self.__send_request(sms_type='get_local_list_version', data=kwargs)
        return self._call_result.GetLocalListVersionPayload(list_version=response.get('list_version', 1))

    @on(action=Action.Heartbeat)
    async def on_heartbeat(self, **kwargs):
        await self.__send_request(sms_type='heartbeat')  # there is no arg from response
        return self._call_result.HeartbeatPayload(current_time=datetime.utcnow().isoformat())

    @on(action=Action.MeterValues)
    async def on_meter_values(self, **kwargs):
        await self.__send_request(sms_type='meter_values', data=kwargs)  # there is no arg from response
        return self._call_result.MeterValuesPayload()

    @on(action=Action.ReserveNow)
    async def on_reserve_now(self, **kwargs):
        response = await self.__send_request(sms_type='reserve_now', data=kwargs)
        return self._call_result.ReserveNowPayload(status=response.get('status', ReservationStatus.rejected))

    @on(action=Action.Reset)
    async def on_reset_charger(self, **kwargs):
        response = await self.__send_request(sms_type='reset', data=kwargs)
        return self._call_result.ResetPayload(status=response.get('status', ResetStatus.rejected))

    @on(action=Action.StartTransaction)
    async def on_start_transaction(self, **kwargs):
        response = await self.__send_request(sms_type='start_transaction', data=kwargs)
        return self._call_result.StartTransactionPayload(
            transaction_id=response.get('transaction_id'),
            id_tag_info=IdTagInfo(
                status=response["id_tag_info"].get("status", AuthorizationStatus.invalid),
                parent_id_tag=response["id_tag_info"].get("id_tag", None),
                expiry_date=response["id_tag_info"].get("expiry_date", None)
            )
        )

    @on(action=Action.StatusNotification)
    async def on_status_notification(self, **kwargs):
        await self.__send_request(sms_type='status_notification', data=kwargs)  # there is no arg from response
        return self._call_result.StatusNotificationPayload()

    @on(action=Action.StopTransaction)
    async def on_stop_transaction(self, **kwargs):
        response = await self.__send_request(sms_type='stop_transaction', data=kwargs)
        return self._call_result.StopTransactionPayload(
            id_tag_info=IdTagInfo(
                status=response['id_tag_info'].get('status', AuthorizationStatus.invalid),
                parent_id_tag=response['id_tag_info'].get('id_tag'),
                expiry_date=response['id_tag_info'].get('expiry_date', None)
            ) if response.get('id_tag_info') else None
        )

    @on(action=Action.TriggerMessage)
    async def on_trigger_message(self, **kwargs):
        response = await self.__send_request(sms_type='trigger_message', data=kwargs)
        return self._call_result.TriggerMessagePayload(
            status=response.get('status', TriggerMessageStatus.not_implemented)
        )

    @on(action=Action.UnlockConnector)
    async def on_unlock_connector(self, **kwargs):
        response = await self.__send_request(sms_type='unlock_connector', data=kwargs)
        return self._call_result.UnlockConnectorPayload(status=response.get('status', UnlockStatus.not_supported))

    @on(action=Action.UpdateFirmware)
    async def on_update_firmware(self, **kwargs):
        await self.__send_request(sms_type='update_firmware', data=kwargs)
        return self._call_result.UpdateFirmwarePayload()  # there is no arg from response

    async def send_cancel_reservation_command(self, reservation_id: int):
        payload = call.CancelReservationPayload(reservation_id=reservation_id)
        return await self.call(payload=payload)

    async def send_change_change_availability_command(self, connector_id: int, availability_type: AvailabilityType):
        payload = call.ChangeAvailabilityPayload(connector_id=connector_id, type=availability_type)
        return await self.call(payload=payload)

    async def send_change_configration_command(self, key: str, value: str):
        payload = call.ChangeConfigurationPayload(key=key, value=value)
        return await self.call(payload)

    async def send_clear_cache_command(self):
        payload = call.ClearCachePayload()
        return await self.call(payload)

    async def send_clear_charging_profile_command(
            self, charging_profile_id: int = None, connector_id: int = None,
            charging_profile_purpose: ChargingProfilePurposeType = None, stack_level: int = None
    ):
        payload = call.ClearChargingProfilePayload(
            id=charging_profile_id,
            connector_id=connector_id,
            charging_profile_purpose=charging_profile_purpose,
            stack_level=stack_level
        )
        return await self.call(payload)

    async def send_data_transfer_command(self, vendor_id: str, message_id: str = None, data: str = None):
        payload = call.DataTransferPayload(vendor_id=vendor_id, message_id=message_id, data=data)
        return await self.call(payload)

    async def send_get_composite_schedule_command(
            self, connector_id: int, duration: int, charging_rate_unit: ChargingRateUnitType = None
    ):
        payload = call.GetCompositeSchedulePayload(
            connector_id=connector_id, duration=duration, charging_rate_unit=charging_rate_unit
        )
        return await self.call(payload=payload)

    async def send_change_configuration_command(self, key: str, value: str):
        payload = call.ChangeConfigurationPayload(key=key, value=value)
        return await self.call(payload=payload)

    async def send_get_diagnostics_command(
            self, location: str, retries: int = None, retry_interval: int = None,
            start_time: str = None, stop_time: str = None
    ):
        payload = call.GetDiagnosticsPayload(
            location=location, retries=retries,
            retry_interval=retry_interval, start_time=start_time, stop_time=stop_time
        )
        return await self.call(payload=payload)

    async def send_get_local_version_command(self):
        payload = call.GetLocalListVersionPayload()
        return await self.call(payload=payload)

    async def send_remote_start_transaction_command(self, connector_id: int, id_tag: str):
        payload = call.RemoteStartTransactionPayload(connector_id=connector_id, id_tag=id_tag)
        try:
            return await self.call(payload=payload)
        except Exception:
            return self._call_result.RemoteStartTransactionPayload(status=RemoteStartStopStatus.rejected)

    async def send_remote_stop_transaction_command(self, transaction_id: int):
        payload = call.RemoteStopTransactionPayload(transaction_id=transaction_id)
        try:
            return await self.call(payload=payload)
        except Exception:
            return "Rejected"

    async def send_reverse_now_command(
            self, connector_id: int, expiry_date: str,
            id_tag: str, reservation_id: int, parent_id_tag: str = None):
        payload = call.ReserveNowPayload(
            connector_id=connector_id, expiry_date=expiry_date,
            id_tag=id_tag, reservation_id=reservation_id, parent_id_tag=parent_id_tag
        )
        return await self.call(payload=payload)

    async def send_reset_command(self, reset_type: ResetType):
        payload = call.ResetPayload(type=reset_type)
        return await self.call(payload=payload)

    async def send_local_list_command(self, list_version, update_type: UpdateType, local_authorization_list: list):
        payload = call.SendLocalListPayload(
            list_version=list_version, update_type=update_type, local_authorization_list=local_authorization_list
        )
        return await self.call(payload=payload)

    async def send_charging_profile_command(self, connector_id: int, cs_charging_profiles: dict):
        payload = call.SetChargingProfilePayload(connector_id=connector_id, cs_charging_profiles=cs_charging_profiles)
        return await self.call(payload=payload)

    async def send_trigger_message_command(self, requested_message: MessageTrigger, connector_id: int = None):
        payload = call.TriggerMessagePayload(connector_id=connector_id, requested_message=requested_message)
        return await self.call(payload=payload)

    async def send_unlock_connector_command(self, connector_id):
        payload = call.UnlockConnectorPayload(connector_id=connector_id)
        return await self.call(payload=payload)

    async def __send_request(self, sms_type: str, data: dict = None) -> dict:
        async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=2),
                headers={"Content-Type": "application/json"}
        ) as session:
            try:
                async with session.post(
                        url=OCPP_RAW_MESSAGES_SERVICE_URL.format(self.id, sms_type),
                        json=data
                ) as response:
                    if response.ok: return await response.json()
            except Exception as ex:  # except all Exception to prevent losing connection with Charge Point
                print(ex)
        return {}
