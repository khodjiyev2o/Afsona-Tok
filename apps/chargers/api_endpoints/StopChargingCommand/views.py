import requests
from django.utils import timezone

from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, get_object_or_404
from django.conf import settings
from apps.chargers.models import ChargingTransaction, ChargeCommand
from apps.chargers.api_endpoints.StopChargingCommand.serializers import StopChargingCommandSerializer, \
    StopChargingCommandResponseSerializer

from apps.chargers.utils import generate_id_tag


class StopChargingCommandView(CreateAPIView):
    queryset = ChargeCommand.objects.all()
    serializer_class = StopChargingCommandSerializer

    def create(self, request, *args, **kwargs):
        transaction = get_object_or_404(ChargingTransaction, pk=request.data.get('transaction'))

        command: ChargeCommand = self.queryset.create(
            initiator=ChargeCommand.Initiator.USER,
            user_id=transaction.user_id,
            connector_id=transaction.connector_id,
            user_car=transaction.user_car,
            command=ChargeCommand.Commands.REMOTE_STOP_TRANSACTION,
            id_tag=generate_id_tag()
        )

        is_delivered: bool = command.send_command_stop_to_ocpp_service()

        command.is_delivered = is_delivered
        command.delivered_at = timezone.now()

        serializer = StopChargingCommandResponseSerializer(command)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


__all__ = ['StopChargingCommandView']
