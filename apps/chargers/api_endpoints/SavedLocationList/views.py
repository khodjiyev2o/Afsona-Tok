from django.db.models import Exists
from rest_framework import generics
from apps.chargers.models import Location
from apps.common.models import SavedLocation
from apps.chargers.api_endpoints.LocationList.serializers import LocationListSerializer


class SavedLocationListView(generics.ListAPIView):
    serializer_class = LocationListSerializer
    queryset = Location.objects.all()
    search_fields = ('name', 'address', 'district__name')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = (
            queryset.select_related('district')
            .prefetch_related('chargers', 'chargers__connectors')
            .annotate(used=Exists(queryset=SavedLocation.objects.filter(user_id=self.request.user.id)))
        )
        return queryset

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        return queryset.filter(used=True)

    def get_serializer_context(self):
        # Get latitude and longitude from request parameters
        latitude = self.request.query_params.get('user_latitude')
        longitude = self.request.query_params.get('user_longitude')

        # Create a context dictionary with latitude and longitude
        context = super().get_serializer_context()
        context['user_latitude'] = latitude
        context['user_longitude'] = longitude
        return context


__all__ = ['SavedLocationListView']
