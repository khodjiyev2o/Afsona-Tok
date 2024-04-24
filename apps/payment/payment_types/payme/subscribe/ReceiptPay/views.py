from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.payment.models import Transaction
from apps.payment.payment_types.payme.subscribe.ReceiptPay.serializers import ReceiptCreateAndPaySerializer


class ReceiptPayView(generics.CreateAPIView):
    serializer_class = ReceiptCreateAndPaySerializer
    queryset = Transaction.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


__all__ = ['ReceiptPayView']
