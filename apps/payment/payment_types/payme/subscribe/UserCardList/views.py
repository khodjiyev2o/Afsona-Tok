from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.payment.models import UserCard
from .serializers import UserCardListSerializer


class UserCardListView(generics.ListAPIView):
    serializer_class = UserCardListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserCard.objects.filter(user=self.request.user, status=UserCard.CardChoices.ACTIVE, is_confirmed=True)


__all__ = ['UserCardListView']
