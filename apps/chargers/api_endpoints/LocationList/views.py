from django.db.models import Exists
from rest_framework import generics

from apps.chargers.models import Location
from apps.common.models import SavedLocation

from apps.chargers.api_endpoints.LocationList.serializers import LocationListSerializer


class LocationListView(generics.ListAPIView):
    """List of locations, send user_latitude and user_longitude
    as query parameters to get distance from user location"""
    serializer_class = LocationListSerializer
    search_fields = ('name', 'address', 'district__name')

    def get_queryset(self):
        return Location.objects.select_related('district').prefetch_related(
            'chargers', 'chargers__connectors')

    def get_serializer_context(self):
        # Get latitude and longitude from request parameters
        latitude = self.request.query_params.get('user_latitude')
        longitude = self.request.query_params.get('user_longitude')

        # Create a context dictionary with latitude and longitude
        context = super().get_serializer_context()
        context['user_latitude'] = latitude
        context['user_longitude'] = longitude
        return context


__all__ = ['LocationListView']
