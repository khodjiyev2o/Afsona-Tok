from rest_framework import generics

from apps.chargers.api_endpoints.LocationList.serializers import LocationListSerializer
from apps.chargers.models import Location


class SavedLocationListAPIView(generics.ListAPIView):
    """List of locations, send user_latitude and user_longitude
    as query parameters to get distance from user location"""
    serializer_class = LocationListSerializer
    queryset = Location.objects.all()
    search_fields = ('name', 'address', 'district__name')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(saved_locations__user=self.request.user)
        return queryset.select_related('district').prefetch_related('chargers', 'chargers__connectors')

    def get_serializer_context(self):
        # Get latitude and longitude from request parameters
        latitude = self.request.query_params.get('user_latitude')
        longitude = self.request.query_params.get('user_longitude')

        # Create a context dictionary with latitude and longitude
        context = super().get_serializer_context()
        context['user_latitude'] = latitude
        context['user_longitude'] = longitude
        return context


__all__ = ['SavedLocationListAPIView']
