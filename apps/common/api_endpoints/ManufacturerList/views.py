from rest_framework import generics

from apps.common.api_endpoints.ManufacturerList.serializers import ManufacturerListSerializer
from apps.common.models import Manufacturer


class ManufacturerListView(generics.ListAPIView):
    queryset = Manufacturer.objects.all().order_by('created_at')
    serializer_class = ManufacturerListSerializer
    search_fields = ['name']


__all__ = ['ManufacturerListView']
