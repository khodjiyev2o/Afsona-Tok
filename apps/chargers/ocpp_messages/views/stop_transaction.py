import json
import logging
from decimal import Decimal
from typing import Union

from django.utils import timezone
from ocpp.v16.enums import AuthorizationStatus
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.chargers.models import ChargingTransaction, OCPPServiceRequestResponseLogs

logger = logging.getLogger("telegram")


class StopTransactionAPIView(APIView):
    def dispatch(self, request, *args, **kwargs):
        data = request.body.decode('utf-8')
        charger_id = request.resolver_match.captured_kwargs.get('charger_identify')

        response = super().dispatch(request, *args, **kwargs)
        OCPPServiceRequestResponseLogs.objects.create(
            charger_id=charger_id,
            request_action="StopTransaction",
            request_body=json.loads(data),
            response_body=response.data
        )
        return response

    def post(self, request, *args, **kwargs):
        initial_response = dict(id_tag_info=dict(status=AuthorizationStatus.invalid.value, id_tag=None, expiry_date=None))
        transaction_id = request.data.get("transaction_id")
        meter_stop = request.data.get("meter_stop")
        reason = request.data.get('reason')
        battery_percent_on_stop = self.get_battery_percent_on_stop(request.data)

        charging_transaction: ChargingTransaction = ChargingTransaction.objects.filter(
            pk=transaction_id, status=ChargingTransaction.Status.IN_PROGRESS
        ).select_related('user').first()
        if not charging_transaction:
            logger.error(f"StopTransaction: {transaction_id} Not Found")
            return Response(initial_response, status=status.HTTP_200_OK)

        charging_transaction.meter_on_end = meter_stop
        charging_transaction.meter_used = round(
            (charging_transaction.meter_on_end - charging_transaction.meter_on_start) / 1000, 2
        )
        charging_transaction.total_price = charging_transaction.price_per_kwh * Decimal(str(charging_transaction.meter_used))
        charging_transaction.status = ChargingTransaction.Status.FINISHED
        charging_transaction.end_time = timezone.now()
        charging_transaction.stop_reason = reason
        charging_transaction.battery_percent_on_end = battery_percent_on_stop if battery_percent_on_stop else charging_transaction.battery_percent_on_end

        charging_transaction.save(update_fields=[
            "meter_on_start", "meter_used", "total_price",
            "status", "end_time", "stop_reason", 'battery_percent_on_end'
        ])

        charging_transaction.user.update_balance()

        initial_response['id_tag_info']['status'] = AuthorizationStatus.accepted.value
        return Response(data=initial_response, status=status.HTTP_200_OK)

    @staticmethod
    def get_battery_percent_on_stop(data: dict) -> Union[int, None]:
        transaction_data = data.get('transaction_data')
        for data in transaction_data:
            context = data.get('context')
            measurand = data.get('measurand')
            location = data.get('location')
            if all([context == 'Transaction.End', measurand == 'SoC', location == 'EV']):
                return int(data.get('value'))
