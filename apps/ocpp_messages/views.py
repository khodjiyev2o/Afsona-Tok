import logging

from django.utils import timezone
from ocpp.v16.enums import RegistrationStatus, AuthorizationStatus
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.chargers.models import ChargePoint, ChargingTransaction, ChargeCommand

logger = logging.getLogger("telegram")


class ChargerDisconnectAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        print(kwargs)
        return Response({}, status=200)


class BootNotificationAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data

        return Response({"interval": 10, "status": RegistrationStatus.accepted}, status=200)


class StatusNotificationAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        return Response(status=200)


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
        meter_values = request.data['meter_value'][0]['sampled_value']
        transaction_id = request.data['transaction_id']

        transaction = ChargingTransaction.objects.filter(status=ChargingTransaction.Status.IN_PROGRESS,
                                                         pk=transaction_id).first()  # noqa
        if not transaction:
            logger.error(f"MeterValues: {transaction_id} Not Found")

        mapping = {"SoC": "battery_percent_on_end", "Energy.Active.Import.Register": "meter_on_end"}
        for meter_value in meter_values:
            measurand = meter_value.get("measurand")
            value = meter_value.get("value")
            if meter_value in mapping: setattr(transaction, mapping[measurand], int(value))  # noqa
            if not transaction.battery_percent_on_start and measurand == 'SoC': transaction.battery_percent_on_start = int(
                value)  # noqa
        transaction.save(update_fields=["battery_percent_on_end", "meter_on_end", "battery_percent_on_start"])
        return Response(data={}, status=200)


class StartTransactionAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        initial_response = {
            "transaction_id": -1,
            "id_tag_info":
                {"status": AuthorizationStatus.invalid, "id_tag": "random_string_len_20", "expiry_date": None}
        }

        charger_id, connector_id = kwargs.get("charger_identify"), data.get("connector_id")
        id_tag, meter_start = data.get("id_tag"), data.get('meter_start')

        command: ChargeCommand = ChargeCommand.objects.filter(id_tag=id_tag).first()  # todo filter by done_at
        if not command:
            return Response(initial_response, status=200)

        charging_transaction = ChargingTransaction.objects.create(
            user_id=command.user_id, user_car_id=command.user_car_id, connector_id=command.connector_id,
            start_reason=ChargingTransaction.StartReason.REMOTE, meter_on_start=meter_start
        )
        initial_response['transaction_id'] = charging_transaction.id
        initial_response['id_tag_info']['status'] = AuthorizationStatus.accepted
        return Response(initial_response, status=200)


class StopTransactionAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        return Response(status=200)


class CommandCallbackAPIView(APIView):
    def post(self, request, *args, **kwargs):
        print(request.data)
        return Response(data={}, status=200)
