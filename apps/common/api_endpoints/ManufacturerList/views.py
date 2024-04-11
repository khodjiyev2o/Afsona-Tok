from rest_framework import generics

from apps.common.models import Manufacturer
from apps.common.api_endpoints.ManufacturerList.serializers import ManufacturerListSerializer


class ManufacturerListView(generics.ListAPIView):
    queryset = Manufacturer.objects.all().order_by('created_at')
    serializer_class = ManufacturerListSerializer


__all__ = ['ManufacturerListView']
