import logging
from decimal import Decimal

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.chargers.models import ChargingTransaction
from apps.chargers.ocpp_messages.views.utils import get_price_from_settings
from apps.chargers.tasks import send_remote_stop_command_to_ocpp_service

logger = logging.getLogger("telegram")

PRICE = get_price_from_settings()


class MeterValuesAPIView(APIView):
    def post(self, request, *args, **kwargs):
        meter_values = request.data.get('meter_value', [{}])[0].get('sampled_value', [])
        transaction_id = request.data.get('transaction_id', None)

        transaction: ChargingTransaction = ChargingTransaction.objects.filter(
            pk=transaction_id, status=ChargingTransaction.Status.IN_PROGRESS
        ).first()
        if not transaction:
            logger.error(f"MeterValues: Transaction: {transaction_id} Not Found")
            return Response(data={}, status=status.HTTP_200_OK)

        mapping = {"SoC": "battery_percent_on_end", "Energy.Active.Import.Register": "meter_on_end"}
        for meter_value in meter_values:
            measurand = meter_value.get("measurand")
            value = meter_value.get("value")
            if measurand in mapping: setattr(transaction, mapping[measurand], int(value))  # noqa
        transaction.save(update_fields=["battery_percent_on_end", "meter_on_end", "battery_percent_on_start"])
        if self.check_limit_reached(transaction):
            send_remote_stop_command_to_ocpp_service.delay(transaction.id)

        return Response(data={}, status=status.HTTP_200_OK)

    @staticmethod
    def check_limit_reached(transaction: ChargingTransaction) -> bool:
        if not transaction.is_limited:
            return False

        user_balance_reached = False
        money_until_now = Decimal(str(transaction.consumed_kwh)) * PRICE

        is_limit_reached = money_until_now >= transaction.limited_money
        if transaction.user: user_balance_reached = money_until_now >= transaction.user.balance # noqa

        return is_limit_reached or user_balance_reached

