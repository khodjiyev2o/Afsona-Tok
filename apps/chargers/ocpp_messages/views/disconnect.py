import json
import logging

from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.chargers.models import ChargePoint, Connector, OCPPServiceRequestResponseLogs

logger = logging.getLogger("telegram")


class ChargerDisconnectAPIView(APIView):
    def dispatch(self, request, *args, **kwargs):
        data = request.body.decode('utf-8')
        charger_id = request.resolver_match.captured_kwargs.get('charger_identify')

        response = super().dispatch(request, *args, **kwargs)
        OCPPServiceRequestResponseLogs.objects.create(
            charger_id=charger_id,
            request_action="Disconnect",
            request_body=json.loads(data),
            response_body=response.data
        )
        return response

    def post(self, request, *args, **kwargs):
        charger_id = kwargs.get("charger_identify")
        reason = request.data.get("reason")

        Connector.objects.filter(
            Q(charge_point__charger_id=charger_id) & ~Q(status=Connector.Status.CHARGING)
        ).update(
            status=Connector.Status.UNAVAILABLE, last_status_reason=Connector.LastStatusReason.CHARGER_DISCONNECTED
        )

        ChargePoint.objects.filter(charger_id=charger_id).update(is_connected=False)
        logger.info(f"Disconnect: {charger_id}\nReason: {reason}")

        return Response(data={}, status=status.HTTP_200_OK)
