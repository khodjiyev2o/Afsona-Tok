from rest_framework import generics
from apps.common.models import CarModel
from apps.common.api_endpoints.CarModelList.serializers import CarModelListSerializer


class CarModelListView(generics.ListAPIView):
    """Send manufacturer_id in query params to get list of car models"""
    serializer_class = CarModelListSerializer

    def get_queryset(self):
        return CarModel.objects.filter(manufacturer__id=self.kwargs['manufacturer_id']).order_by('created_at')


__all__ = ['CarModelListView']
