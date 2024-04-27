import logging

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from apps.chargers.models import ChargeCommand
from apps.chargers.ocpp_messages.serializers import CommandCallbackSerializer

logger = logging.getLogger("telegram")


class CommandCallbackAPIView(CreateAPIView):
    queryset = ChargeCommand.objects.all()
    serializer_class = CommandCallbackSerializer

    def create(self, request, *args, **kwargs):
        id_tag = kwargs.get('id_tag')
        command: ChargeCommand = ChargeCommand.objects.filter(id_tag=id_tag).first()

        if not command:
            logger.error(f"CommandCallback: Id tag {id_tag} not found")
            return Response(data={}, status=status.HTTP_200_OK)
        command.done_at = timezone.now()
        command.status = request.data.get('status')
        command.save(update_fields=['done_at', 'status'])

        payload = {
            'type': 'send_command_result',
            'status': command.status,
            'id': command.id
        }
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(group=f'user_id_{command.user_id}', message=payload) # noqa

        return Response(data={}, status=status.HTTP_200_OK)
