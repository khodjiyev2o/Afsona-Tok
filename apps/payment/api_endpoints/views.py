from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.payment.models import Transaction
from apps.payment.api_endpoints.serializers import TransactionCreateSerializer


class TransactionCreateView(generics.CreateAPIView):
    serializer_class = TransactionCreateSerializer
    queryset = Transaction.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


__all__ = ['TransactionCreateView']
