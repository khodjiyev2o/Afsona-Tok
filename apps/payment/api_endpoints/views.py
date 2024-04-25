from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.payment.models import Transaction
from apps.payment.api_endpoints.serializers import TransactionCreateSerializer, TransactionDetailSerializer


class TransactionCreateView(generics.CreateAPIView):
    serializer_class = TransactionCreateSerializer
    queryset = Transaction.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TransactionDetailView(generics.RetrieveAPIView):
    serializer_class = TransactionDetailSerializer
    queryset = Transaction.objects.all()
    permission_classes = [IsAuthenticated]


__all__ = ['TransactionCreateView', 'TransactionDetailView']
