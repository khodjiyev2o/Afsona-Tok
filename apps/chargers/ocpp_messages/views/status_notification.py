import logging
from decimal import Decimal

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from apps.chargers.models import Connector, ChargingTransaction
from apps.chargers.ocpp_messages.views.utils import get_price_from_settings

logger = logging.getLogger("telegram")

PRICE = get_price_from_settings()


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
        # if connector.status == Connector.Status.FAULTED:
        #     self.stop_in_progress_transaction_on_faulted(connector)

        return Response(data={}, status=status.HTTP_200_OK)

    @staticmethod
    def stop_in_progress_transaction_on_faulted(connector: Connector):
        charging_transaction = ChargingTransaction.objects.filter(
            status=ChargingTransaction.Status.IN_PROGRESS,
            connector=connector
        ).last()

        if not charging_transaction:
            return
        charging_transaction.meter_used = round(
            (charging_transaction.meter_on_end - charging_transaction.meter_on_start) / 1000, 2
        )
        charging_transaction.total_price = PRICE * Decimal(str(charging_transaction.meter_used))
        charging_transaction.status = ChargingTransaction.Status.FINISHED
        charging_transaction.end_time = timezone.now()
        charging_transaction.stop_reason = ChargingTransaction.StopReason.CONNECTOR_ERROR
        charging_transaction.save(update_fields=['meter_used', 'total_price', 'status', 'end_time', 'stop_reason'])

        user = charging_transaction.user
        if user:
            user.balance -= charging_transaction.total_price
            user.save(update_fields=['balance'])
