import time

import requests
from django.utils import timezone

from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.chargers.models import ChargeCommand
from apps.chargers.api_endpoints.StartChargingCommand.serializers import StartChargingCommandSerializer
from apps.chargers.utils import generate_id_tag


class StartChargingCommandView(CreateAPIView):
    queryset = ChargeCommand.objects.all()
    serializer_class = StartChargingCommandSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        command: ChargeCommand = self.queryset.create(
            **serializer.validated_data,
            id_tag=generate_id_tag(),
            command=ChargeCommand.Commands.REMOTE_START_TRANSACTION,
            user_id=request.user.id
        )
        is_delivered: bool = self._send_command_start_to_ocpp_service(command)

        command.is_delivered = is_delivered
        command.delivered_at = timezone.now()
        command.save(update_fields=['is_delivered', 'delivered_at'])

        serializer = self.get_serializer(command)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def _send_command_start_to_ocpp_service(command: ChargeCommand) -> bool:
        timeout = 2
        retry = 3
        retry_delay = 0.2

        url = 'http://localhost:8080/ocpp/http/commands/remote_start/'
        payload = {
            "id_tag": command.id_tag,
            "charger_identify": command.connector.charge_point.charger_id,
            "connector_id": command.connector.connector_id
        }

        for _ in range(retry):
            try:
                response = requests.post(url=url, json=payload, timeout=timeout)
            except Exception as e:
                time.sleep(retry_delay)
                continue

            is_delivered: bool = response.json().get('status')
            if is_delivered:
                return True
            time.sleep(retry_delay)
        return False


__all__ = ['StartChargingCommandView']
