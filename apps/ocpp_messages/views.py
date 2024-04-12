import logging
from decimal import Decimal
from channels.layers import get_channel_layer

from asgiref.sync import async_to_sync
from django.db.models import Q
from django.utils import timezone
from ocpp.v16.enums import RegistrationStatus, AuthorizationStatus
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from apps.chargers.models import ChargePoint, ChargingTransaction, ChargeCommand, Connector

logger = logging.getLogger("telegram")

PRICE = Decimal('2000')


class ChargerDisconnectAPIView(APIView):
    def post(self, request, *args, **kwargs):
        charger_id = kwargs.get("charger_identify")
        reason = request.data.get("reason")

        Connector.objects.filter(
            Q(charge_point__charger_id=charger_id) & ~Q(status=Connector.Status.CHARGING)
        ).update(
            status=Connector.Status.UNAVAILABLE, last_status_reason=Connector.LastStatusReason.CHARGER_DISCONNECTED
        )

        ChargePoint.objects.filter(charger_id=charger_id).update(is_connected=False)
        logger.info(f"Disconnect: {charger_id}\nReason: {reason}")

        return Response(data={}, status=status.HTTP_200_OK)


class BootNotificationAPIView(APIView):
    def post(self, request, *args, **kwargs):
        initial_response = {"interval": 10, "status": RegistrationStatus.rejected}
        charger_id = kwargs.get("charger_identify")
        charge_point: ChargePoint = ChargePoint.objects.filter(charger_id=charger_id, is_connected=False).first()

        if not charge_point:
            logger.error(f"BootNotification: {charger_id} Not Found")
            return Response(data=initial_response, status=status.HTTP_200_OK)

        charge_point.is_connected = True
        charge_point.last_boot_notification = timezone.now()
        charge_point.save(update_fields=['is_connected', 'last_boot_notification'])

        logger.info(f"BootNotification: {charger_id}")
        initial_response['status'] = RegistrationStatus.accepted
        return Response(initial_response, status=status.HTTP_200_OK)


class StatusNotificationAPIView(APIView):
    def post(self, request, *args, **kwargs):
        charger_identify = kwargs.get("charger_identify")
        connector_id = request.data.get("connector_id")
        connector_status = request.data.get("status")
        error_code = request.data.get("error_code")

        connector: Connector = Connector.objects.filter(
            charge_point__charger_id=charger_identify, connector_id=connector_id
        ).first()
        if not connector:
            logger.error(
                f"StatusNotification: Charger {charger_identify} -> {connector_id} -> {connector_status} Not Found"
            )
            return Response(data={}, status=status.HTTP_200_OK)

        connector.status = connector_status
        connector.last_status_reason = Connector.LastStatusReason.NORMAL
        connector.save(update_fields=['status', 'last_status_reason'])

        if error_code != "NoError":
            logger.error(f"StatusNotification: Charger {charger_identify} -> {connector_id} -> {error_code}")
        return Response(data={}, status=status.HTTP_200_OK)


class HeartbeatAPIView(APIView):
    def post(self, request, *args, **kwargs):
        charger_identify = kwargs.get("charger_identify")

        charge_point: ChargePoint = ChargePoint.objects.filter(charger_id=charger_identify).first()
        if not charge_point:
            logger.error(msg=f"Heartbeat: {charger_identify} does not exists")
            return Response(status=200)

        charge_point.last_heartbeat = timezone.now()
        charge_point.is_connected = True
        charge_point.save(update_fields=['last_heartbeat', 'is_connected'])

        logger.info(f"Heartbeat:  {charger_identify}")
        return Response(status=200)


class MeterValuesAPIView(APIView):
    def post(self, request, *args, **kwargs):
        meter_values = request.data.get('meter_value', [{}])[0].get('sampled_value', [])
        transaction_id = request.data.get('transaction_id', None)

        transaction = ChargingTransaction.objects.filter(
            pk=transaction_id, status=ChargingTransaction.Status.IN_PROGRESS
        ).first()
        if not transaction:
            logger.error(f"MeterValues: Transaction: {transaction_id} Not Found")
            return Response(data={}, status=status.HTTP_200_OK)

        mapping = {"SoC": "battery_percent_on_end", "Energy.Active.Import.Register": "meter_on_end"}
        for meter_value in meter_values:
            measurand = meter_value.get("measurand")
            value = meter_value.get("value")
            if meter_value in mapping: setattr(transaction, mapping[measurand], int(value))  # noqa
        transaction.save(update_fields=["battery_percent_on_end", "meter_on_end", "battery_percent_on_start"])
        return Response(data={}, status=status.HTTP_200_OK)


class StartTransactionAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        initial_response = {
            "transaction_id": -1,
            "id_tag_info":
                {"status": AuthorizationStatus.invalid, "id_tag": None, "expiry_date": None}
        }

        charger_id, connector_id = kwargs.get("charger_identify"), data.get("connector_id")
        id_tag, meter_start = data.get("id_tag"), data.get('meter_start')

        command: ChargeCommand = ChargeCommand.objects.filter(id_tag=id_tag).first()
        connector = Connector.objects.filter(charge_point__charger_id=charger_id, connector_id=connector_id).first()
        if not command and not connector:
            logger.error(
                f"StartTransaction: id tag: {id_tag}  or connector: {charger_id} -> {connector_id} Not Found"
            )
            return Response(initial_response, status=status.HTTP_200_OK)

        charging_transaction = ChargingTransaction.objects.create(
            user_id=command.user_id, user_car_id=command.user_car_id, connector_id=command.connector_id,
            start_reason=ChargingTransaction.StartReason.REMOTE, meter_on_start=meter_start
        )
        initial_response['transaction_id'] = charging_transaction.id
        initial_response['id_tag_info']['status'] = AuthorizationStatus.accepted
        return Response(initial_response, status=status.HTTP_200_OK)


class StopTransactionAPIView(APIView):
    def post(self, request, *args, **kwargs):
        initial_response = dict(id_tag_info=dict(status=AuthorizationStatus.invalid, id_tag=None, expiry_date=None))
        transaction_id = request.data.get("transaction_id")
        meter_stop = request.data.get("meter_stop")
        reason = request.data.get('reason')

        charging_transaction: ChargingTransaction = ChargingTransaction.objects.filter(
            pk=transaction_id, status=ChargingTransaction.Status.IN_PROGRESS
        ).select_related('user').first()
        if not charging_transaction:
            logger.error(f"StopTransaction: {transaction_id} Not Found")
            return Response(initial_response, status=status.HTTP_200_OK)

        charging_transaction.meter_on_end = meter_stop
        charging_transaction.meter_used = round(
            (charging_transaction.meter_on_start - charging_transaction.meter_on_end) / 1000, 2
        )
        charging_transaction.total_price = PRICE * Decimal(str(charging_transaction.meter_used))
        charging_transaction.status = ChargingTransaction.Status.FINISHED
        charging_transaction.stop_reason = reason
        charging_transaction.save(update_fields=['meter_on_start', 'meter_used'])

        user = charging_transaction.user
        user.balance -= charging_transaction.total_price
        user.save(update_fields=['balance'])

        initial_response['id_tag_info']['status'] = AuthorizationStatus.accepted
        return Response(data=initial_response, status=status.HTTP_200_OK)


class CommandCallbackAPIView(APIView):
    def post(self, request, *args, **kwargs):
        id_tag = kwargs.get('id_tag')
        command: ChargeCommand = ChargeCommand.objects.filter(id_tag=id_tag).first()

        if not command:
            logger.error(f"CommandCallback: Id tag {id_tag} not found")
            return Response(data={}, status=status.HTTP_200_OK)
        command.done_at = timezone.now()
        command.status = request.data.get('status')
        command.save(update_fields=['done_at', 'status'])

        payload = {
            'type': 'send_command_result',
            'status': command.status,
            'id': command.id
        }
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(group=f'user_id_{command.user_id}', message=payload)

        return Response(data={}, status=status.HTTP_200_OK)

