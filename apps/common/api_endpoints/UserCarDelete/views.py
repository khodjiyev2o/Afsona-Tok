from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.common.models import UserCar


class UserCarDeleteView(generics.DestroyAPIView):
    queryset = UserCar.objects.all()
    permission_classes = [IsAuthenticated]


__all__ = ['UserCarDeleteView']
