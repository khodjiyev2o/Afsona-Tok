import logging
from decimal import Decimal

from ocpp.v16.enums import AuthorizationStatus
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.chargers.models import ChargingTransaction, ChargeCommand, Connector

logger = logging.getLogger("telegram")

PRICE = Decimal('2000')


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

        cash_mode = True if id_tag == "" else False

        command: ChargeCommand = ChargeCommand.objects.filter(id_tag=id_tag).first()
        connector = Connector.objects.filter(charge_point__charger_id=charger_id, connector_id=connector_id).first()
        if not command and not connector and not cash_mode:
            logger.error(
                f"StartTransaction: id tag: {id_tag}  or connector: {charger_id} -> {connector_id} Not Found"
            )
            return Response(initial_response, status=status.HTTP_200_OK)

        if cash_mode:
            transaction_data = dict(
                user_id=None,
                user_car_id=None,
                start_reason=ChargingTransaction.StartReason.LOCAL
            )
        else:
            transaction_data = dict(
                user_id=command.user_id,
                user_car_id=command.user_car_id,
                start_reason=ChargingTransaction.StartReason.REMOTE
            )

        charging_transaction = ChargingTransaction.objects.create(
            **transaction_data, connector_id=connector.id, meter_on_start=meter_start
        )
        initial_response['transaction_id'] = charging_transaction.id
        initial_response['id_tag_info']['status'] = AuthorizationStatus.accepted
        return Response(initial_response, status=status.HTTP_200_OK)
