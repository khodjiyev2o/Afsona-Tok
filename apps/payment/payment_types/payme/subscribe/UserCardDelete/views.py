from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.payment.models import UserCard
from .serializers import UserCardDeleteSerializer


class UserCardDeleteView(generics.UpdateAPIView):
    queryset = UserCard.objects.all()
    serializer_class = UserCardDeleteSerializer
    permission_classes = [IsAuthenticated]


__all__ = ['UserCardDeleteView']
