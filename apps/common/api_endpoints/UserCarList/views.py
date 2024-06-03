from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.common.api_endpoints.UserCarList.serializers import UserCarListSerializer
from apps.common.models import UserCar


class UserCarListView(generics.ListAPIView):
    serializer_class = UserCarListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (UserCar.objects.filter(user=self.request.user)
                .select_related('manufacturer', 'model').prefetch_related('connector_type')
                )


__all__ = ['UserCarListView']
