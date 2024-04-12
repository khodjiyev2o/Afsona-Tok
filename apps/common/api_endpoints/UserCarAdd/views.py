from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.common.models import UserCar

from apps.common.api_endpoints.UserCarAdd.serializers import UserCarAddSerializer


class UserCarAddView(generics.CreateAPIView):
    """Add user car"""
    serializer_class = UserCarAddSerializer
    queryset = UserCar.objects.all()
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


__all__ = ['UserCarAddView']
