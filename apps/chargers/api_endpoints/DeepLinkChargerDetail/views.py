from rest_framework import generics

from apps.chargers.api_endpoints.DeepLinkChargerDetail.serializers import ChargersDetailSerializer
from apps.chargers.models import ChargePoint


class DeepLinkChargerDetailView(generics.RetrieveAPIView):
    """Detail of location, send user_latitude and user_longitude
    as query parameters to get distance from user location"""
    serializer_class = ChargersDetailSerializer
    queryset = ChargePoint.objects.all()
    lookup_field = 'charger_id'
    lookup_url_kwarg = 'charger_id'


__all__ = ['DeepLinkChargerDetailView']
