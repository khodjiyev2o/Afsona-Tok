import json
import logging

from ocpp.v16.enums import AuthorizationStatus
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.chargers.models import ChargingTransaction, ChargeCommand, Connector, OCPPServiceRequestResponseLogs

logger = logging.getLogger("telegram")


class StartTransactionAPIView(APIView):

    def dispatch(self, request, *args, **kwargs):
        data = request.body.decode('utf-8')
        charger_id = request.resolver_match.captured_kwargs.get('charger_identify')

        response = super().dispatch(request, *args, **kwargs)
        OCPPServiceRequestResponseLogs.objects.create(
            charger_id=charger_id,
            request_action="StartTransaction",
            request_body=json.loads(data),
            response_body=response.data
        )
        return response

    def post(self, request, *args, **kwargs):
        data = request.data
        initial_response = {
            "transaction_id": -1,
            "id_tag_info":
                {"status": AuthorizationStatus.invalid.value, "id_tag": None, "expiry_date": None}
        }

        charger_id, connector_id = kwargs.get("charger_identify"), data.get("connector_id")
        id_tag, meter_start = data.get("id_tag"), data.get('meter_start')

        in_progress_transaction = ChargingTransaction.objects.filter(status=ChargingTransaction.Status.IN_PROGRESS, start_command__id_tag=id_tag).first()
        if in_progress_transaction:
            initial_response['transaction_id'] = in_progress_transaction.id
            initial_response['id_tag_info']['status'] = AuthorizationStatus.accepted.value
            return Response(initial_response, status=status.HTTP_200_OK)

        cash_mode = True if id_tag == "" else False
        id_tag_already_used: bool = True

        command: ChargeCommand = ChargeCommand.objects.filter(id_tag=id_tag).first()
        connector: Connector = Connector.objects.filter(
            charge_point__charger_id=charger_id, connector_id=connector_id
        ).first()
        if not command and not connector and not cash_mode:
            logger.error(
                f"StartTransaction: id tag: {id_tag}  or connector: {charger_id} -> {connector_id} Not Found"
            )
            return Response(initial_response, status=status.HTTP_200_OK)

        if command:
            id_tag_already_used = bool(ChargingTransaction.objects.filter(start_command_id=command.id, status=ChargingTransaction.Status.FINISHED).exists())

        if cash_mode or id_tag_already_used:
            transaction_data = dict(
                user_id=None,
                user_car_id=None,
                start_reason=ChargingTransaction.StartReason.LOCAL
            )
        else:
            transaction_data = dict(
                user_id=command.user_id,
                user_car_id=command.user_car_id,
                start_reason=ChargingTransaction.StartReason.REMOTE,
                is_limited=command.is_limited,
                limited_money=command.limited_money,
                start_command_id=command.id,

            )

        charging_transaction = ChargingTransaction.objects.create(
            **transaction_data, price_per_kwh=connector.charge_point.price_per_kwh,
            connector_id=connector.id, meter_on_start=meter_start
        )
        initial_response['transaction_id'] = charging_transaction.id
        initial_response['id_tag_info']['status'] = AuthorizationStatus.accepted.value
        return Response(initial_response, status=status.HTTP_200_OK)
