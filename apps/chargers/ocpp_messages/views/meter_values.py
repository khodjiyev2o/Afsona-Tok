import logging
from decimal import Decimal

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.chargers.models import ChargingTransaction
from apps.chargers.ocpp_messages.views.utils import get_price_from_settings

logger = logging.getLogger("telegram")

PRICE = get_price_from_settings()


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
            if measurand in mapping: setattr(transaction, mapping[measurand], int(value))  # noqa
        transaction.save(update_fields=["battery_percent_on_end", "meter_on_end", "battery_percent_on_start"])
        return Response(data={}, status=status.HTTP_200_OK)
