from rest_framework import generics
from apps.chargers.models import Location
from apps.chargers.api_endpoints.MapLocationList.serializers import MapLocationListSerializer


class MapLocationListView(generics.ListAPIView):
    """List of locations for map"""
    serializer_class = MapLocationListSerializer
    queryset = Location.objects.all().values('id', 'latitude', 'longitude')


__all__ = ['MapLocationListView']
