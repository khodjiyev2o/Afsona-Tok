from rest_framework import serializers
from apps.payment.models import UserCard, Transaction


class ReceiptCreateAndPay(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = (
            'amount'
        )
