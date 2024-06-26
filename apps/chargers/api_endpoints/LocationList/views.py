from django.db.models import Q
from rest_framework import generics
from rest_framework.response import Response

from apps.chargers.api_endpoints.LocationList.serializers import LocationListSerializer
from apps.chargers.models import Location


class LocationListView(generics.ListAPIView):
    """List of locations, send user_latitude and user_longitude
    as query parameters to get distance from user location"""
    serializer_class = LocationListSerializer
    search_fields = ('name', 'address', 'district__name')

    def get_queryset(self):
        return Location.objects.select_related('district').prefetch_related(
            'chargers', 'chargers__connectors')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if 'search' in request.query_params:
            search = request.query_params.get('search')
            if search:
                queryset = queryset.filter(
                    Q(name__icontains=search) |
                    Q(address__icontains=search) |
                    Q(district__name__icontains=search)
                )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            sorted_data = sorted(serializer.data, key=lambda x: x['distance'])
            return self.get_paginated_response(sorted_data)
        serializer = self.get_serializer(queryset, many=True)
        sorted_data = sorted(serializer.data, key=lambda x: x['distance'])
        return Response(sorted_data)

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
