import logging
from decimal import Decimal

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.chargers.models import Connector

logger = logging.getLogger("telegram")

PRICE = Decimal('2000')


class StatusNotificationAPIView(APIView):
    def post(self, request, *args, **kwargs):
        charger_identify = kwargs.get("charger_identify")
        connector_id = request.data.get("connector_id")
        connector_status = request.data.get("status")
        error_code = request.data.get("error_code")

        connector: Connector = Connector.objects.filter(
            charge_point__charger_id=charger_identify, connector_id=connector_id
        ).first()
        if not connector:
            logger.error(
                f"StatusNotification: Charger {charger_identify} -> {connector_id} -> {connector_status} Not Found"
            )
            return Response(data={}, status=status.HTTP_200_OK)

        connector.status = connector_status
        connector.last_status_reason = Connector.LastStatusReason.NORMAL
        connector.save(update_fields=['status', 'last_status_reason'])

        if error_code != "NoError":
            logger.error(f"StatusNotification: Charger {charger_identify} -> {connector_id} -> {error_code}")
        return Response(data={}, status=status.HTTP_200_OK)
