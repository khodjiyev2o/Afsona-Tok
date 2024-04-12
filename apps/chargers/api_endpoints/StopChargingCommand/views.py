from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, get_object_or_404
import requests
from apps.chargers.models import ChargingTransaction, ChargeCommand
from .serializers import StopChargingCommandSerializer, StopChargingCommandResponseSerializer
from django.utils import timezone

from ...utils import generate_id_tag


class StopChargingCommandView(CreateAPIView):
    queryset = ChargeCommand.objects.all()
    serializer_class = StopChargingCommandSerializer

    def create(self, request, *args, **kwargs):
        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        transaction = get_object_or_404(ChargingTransaction, pk=request.data.get('transaction'))

        command: ChargeCommand = self.queryset.create(
            user_id=transaction.user_id,
            connector_id=transaction.connector_id,
            user_car=transaction.user_car,
            command=ChargeCommand.Commands.REMOTE_STOP_TRANSACTION,
            id_tag=generate_id_tag()
        )

        response = requests.post(
            f'http://localhost:8080/ocpp/http/commands/remote_stop/',
            json={
                "transaction_id": transaction.id,
                "charger_identify": transaction.connector.charge_point.charger_id,
                "id_tag": command.id_tag
            }
        )  # todo add try except for ocpp service down and auth

        command.is_delivered = response.json().get('status')
        command.delivered_at = timezone.now()

        serializer = StopChargingCommandResponseSerializer(command)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
