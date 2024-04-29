from rest_framework import generics
from django.db.models import Exists

from apps.chargers.models import Location
from apps.common.models import SavedLocation

from apps.chargers.api_endpoints.LocationDetail.serializers import LocationDetailSerializer


class LocationDetailView(generics.RetrieveAPIView):
    """Detail of location, send user_latitude and user_longitude
    as query parameters to get distance from user location"""
    serializer_class = LocationDetailSerializer

    def get_queryset(self):
        return Location.objects.select_related('district').prefetch_related(
            'chargers', 'chargers__connectors').annotate(is_favorite=Exists(
            queryset=SavedLocation.objects.filter(user_id=self.request.user.id))).filter(
            chargers__is_visible_in_mobile=True
        )

    def get_serializer_context(self):
        # Get latitude and longitude from request parameters
        latitude = self.request.query_params.get('user_latitude')
        longitude = self.request.query_params.get('user_longitude')

        # Create a context dictionary with latitude and longitude
        context = super().get_serializer_context()
        context['user_latitude'] = latitude
        context['user_longitude'] = longitude
        return context


__all__ = ['LocationDetailView']
