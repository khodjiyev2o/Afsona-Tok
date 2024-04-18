from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.common.models import UserCar
from apps.common.api_endpoints.UserCarList.serializers import UserCarListSerializer


class UserCarListView(generics.ListAPIView):
    serializer_class = UserCarListSerializer
    permission_classes = [IsAuthenticated]
    queryset = UserCar.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user).select_related('manufacturer', 'model')


__all__ = ['UserCarListView']
