import json
import logging
from decimal import Decimal

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.chargers.models import ChargingTransaction, OCPPServiceRequestResponseLogs
from apps.chargers.ocpp_messages.views.utils import get_price_from_settings
from apps.chargers.tasks import send_remote_stop_command_to_ocpp_service

logger = logging.getLogger("telegram")

PRICE = get_price_from_settings()


class MeterValuesAPIView(APIView):
    def dispatch(self, request, *args, **kwargs):
        data = request.body.decode('utf-8')
        charger_id = request.resolver_match.captured_kwargs.get('charger_identify')

        response = super().dispatch(request, *args, **kwargs)
        OCPPServiceRequestResponseLogs.objects.create(
            charger_id=charger_id,
            request_action="MeterValues",
            request_body=json.loads(data),
            response_body=response.data
        )
        return response

    def post(self, request, *args, **kwargs):
        meter_values = request.data.get('meter_value', [{}])[0].get('sampled_value', [])
        transaction_id = request.data.get('transaction_id', None)

        transaction: ChargingTransaction = ChargingTransaction.objects.filter(
            pk=transaction_id, status=ChargingTransaction.Status.IN_PROGRESS
        ).first()
        if not transaction:
            logger.error(f"MeterValues: Transaction: {transaction_id} Not Found")
            return Response(data={}, status=status.HTTP_200_OK)

        is_first_meter_value = transaction.meter_on_end is None

        mapping = {"SoC": "battery_percent_on_end", "Energy.Active.Import.Register": "meter_on_end"}
        for meter_value in meter_values:
            measurand = meter_value.get("measurand")
            value = meter_value.get("value")
            if measurand in mapping: setattr(transaction, mapping[measurand], int(value))  # noqa
        transaction.save(update_fields=["battery_percent_on_end", "meter_on_end", "battery_percent_on_start"])

        if is_first_meter_value:
            transaction.meter_on_start = transaction.meter_on_end
            transaction.battery_percent_on_start = transaction.battery_percent_on_end
            transaction.save(update_fields=['meter_on_start', 'battery_percent_on_start'])

        if self.check_limit_reached(transaction):
            send_remote_stop_command_to_ocpp_service.delay(transaction.id)

        return Response(data={}, status=status.HTTP_200_OK)

    @staticmethod
    def check_limit_reached(transaction: ChargingTransaction) -> bool:
        user_balance_reached = False
        is_limit_reached = False
        money_until_now = Decimal(str(transaction.consumed_kwh)) * PRICE

        if transaction.is_limited: is_limit_reached = money_until_now >= transaction.limited_money  # noqa
        if transaction.user: user_balance_reached = money_until_now >= transaction.user.balance  # noqa

        return is_limit_reached or user_balance_reached
