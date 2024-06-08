import json
import logging
from decimal import Decimal

from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.chargers.models import Connector, ChargingTransaction, OCPPServiceRequestResponseLogs

logger = logging.getLogger("telegram")




class StatusNotificationAPIView(APIView):
    def dispatch(self, request, *args, **kwargs):
        data = request.body.decode('utf-8')
        charger_id = request.resolver_match.captured_kwargs.get('charger_identify')

        response = super().dispatch(request, *args, **kwargs)
        OCPPServiceRequestResponseLogs.objects.create(
            charger_id=charger_id,
            request_action="StatusNotification",
            request_body=json.loads(data),
            response_body=response.data
        )
        return response

    def post(self, request, *args, **kwargs):
        charger_identify = kwargs.get("charger_identify")
        connector_id = request.data.get("connector_id")
        connector_status = request.data.get("status")
        error_code = request.data.get("error_code")

        connector: Connector = Connector.objects.filter(
            charge_point__charger_id=charger_identify, connector_id=connector_id
        ).first()
        if not connector:
            return Response(data={}, status=status.HTTP_200_OK)

        connector.status = connector_status
        connector.last_status_reason = Connector.LastStatusReason.NORMAL
        connector.save(update_fields=['status', 'last_status_reason', 'updated_at'])

        if error_code != "NoError":
            logger.error(f"StatusNotification: Charger {charger_identify} -> {connector_id} -> {error_code}")
        # if connector.status == Connector.Status.FAULTED:
        #     self.stop_in_progress_transaction_on_faulted(connector)

        return Response(data={}, status=status.HTTP_200_OK)

    @staticmethod
    def stop_in_progress_transaction_on_faulted(connector: Connector):
        charging_transaction: ChargingTransaction = ChargingTransaction.objects.filter(
            status=ChargingTransaction.Status.IN_PROGRESS,
            connector=connector
        ).last()

        if not charging_transaction:
            return
        charging_transaction.meter_used = round(
            (charging_transaction.meter_on_end - charging_transaction.meter_on_start) / 1000, 2
        )
        charging_transaction.total_price = charging_transaction.price_per_kwh * Decimal(str(charging_transaction.meter_used))
        charging_transaction.status = ChargingTransaction.Status.FINISHED
        charging_transaction.end_time = timezone.now()
        charging_transaction.stop_reason = ChargingTransaction.StopReason.CONNECTOR_ERROR
        charging_transaction.save(update_fields=['meter_used', 'total_price', 'status', 'end_time', 'stop_reason'])

        charging_transaction.user.update_balance()