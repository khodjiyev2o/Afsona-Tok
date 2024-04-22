import logging
from decimal import Decimal

from django.utils import timezone
from ocpp.v16.enums import RegistrationStatus
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.chargers.models import ChargePoint, Connector

logger = logging.getLogger("telegram")

PRICE = Decimal('2000')


class HeartbeatAPIView(APIView):
    def post(self, request, *args, **kwargs):
        charger_identify = kwargs.get("charger_identify")

        charge_point: ChargePoint = ChargePoint.objects.filter(charger_id=charger_identify).first()
        if not charge_point:
            logger.error(msg=f"Heartbeat: {charger_identify} does not exists")
            return Response(data={}, status=200)

        charge_point.last_heartbeat = timezone.now()
        charge_point.is_connected = True
        charge_point.save(update_fields=['last_heartbeat', 'is_connected'])

        logger.info(f"Heartbeat:  {charger_identify}")
        return Response(data={}, status=200)
