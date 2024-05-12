from math import radians, sin, cos, sqrt, atan2
from decimal import Decimal
from django.db.models import F

from rest_framework import generics

from apps.chargers.models import Location
from apps.chargers.api_endpoints.LocationList.serializers import LocationListSerializer


class LocationListView(generics.ListAPIView):
    serializer_class = LocationListSerializer
    search_fields = ('name', 'address', 'district__name')

    def get_queryset(self):
        user_latitude = Decimal(self.request.query_params.get('user_latitude'))
        user_longitude = Decimal(self.request.query_params.get('user_longitude'))

        queryset = Location.objects.annotate(
            distance=self.calculate_distance(user_latitude, user_longitude, F('latitude'), F('longitude'))
        ).order_by('distance')

        return queryset

    def calculate_distance(self, lat1, lon1, lat2, lon2):
        # Haversine formula to calculate distance
        lat1_rad, lon1_rad = radians(lat1), radians(lon1)
        lat2_rad, lon2_rad = radians(lat2), radians(lon2)

        dlon = lon2_rad - lon1_rad
        dlat = lat2_rad - lat1_rad

        a = sin(dlat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        radius_earth = 6371  # Radius of the Earth in kilometers
        distance_km = radius_earth * c

        return distance_km

    def get_serializer_context(self):
        latitude = self.request.query_params.get('user_latitude')
        longitude = self.request.query_params.get('user_longitude')

        context = super().get_serializer_context()
        context['user_latitude'] = latitude
        context['user_longitude'] = longitude
        return context


__all__ = ['LocationListView']