from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.payment.models import UserCard
from apps.payment.payment_types.payme.subscribe.CardCreate.serializers import CarCreateSerializer


class UserCardCreateView(generics.CreateAPIView):
    """
    expire_date in dd/mm format, like: 0726
    """
    queryset = UserCard.objects.all()
    serializer_class = CarCreateSerializer
    permission_classes = [IsAuthenticated]


__all__ = ['UserCardCreateView']
