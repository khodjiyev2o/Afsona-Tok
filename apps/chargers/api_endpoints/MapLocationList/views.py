from rest_framework import generics
from apps.chargers.models import Location
from apps.chargers.api_endpoints.MapLocationList.serializers import MapLocationListSerializer


class MapLocationListView(generics.ListAPIView):
    """List of locations for map"""
    serializer_class = MapLocationListSerializer
    queryset = Location.objects.all().values('id', 'latitude', 'longitude')

    def get_queryset(self):
        queryset = self.queryset
        connector_types = self.request.query_params.getlist('connector_types', [])
        if connector_types:
            queryset = Location.objects.filter(
                chargers__connectors__standard__id__in=connector_types
            ).distinct().values('id', 'latitude', 'longitude')

        return queryset


__all__ = ['MapLocationListView']
