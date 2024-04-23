import logging
from decimal import Decimal

from django.utils import timezone
from ocpp.v16.enums import RegistrationStatus
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.chargers.models import ChargePoint

logger = logging.getLogger("telegram")


class BootNotificationAPIView(APIView):
    def post(self, request, *args, **kwargs):
        initial_response = {"interval": 10, "status": RegistrationStatus.rejected}
        charger_id = kwargs.get("charger_identify")
        charge_point: ChargePoint = ChargePoint.objects.filter(charger_id=charger_id, is_connected=False).first()

        if not charge_point:
            logger.error(f"BootNotification: {charger_id} Not Found")
            return Response(data=initial_response, status=status.HTTP_200_OK)

        charge_point.is_connected = True
        charge_point.last_boot_notification = timezone.now()
        charge_point.save(update_fields=['is_connected', 'last_boot_notification'])

        logger.info(f"BootNotification: {charger_id}")
        initial_response['status'] = RegistrationStatus.accepted
        return Response(initial_response, status=status.HTTP_200_OK)
