from rest_framework import serializers

from apps.payment.models import Transaction


class TransactionCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = (
            'card',
            'amount',
            'payment_type',
            'payment_url'
        )
        extra_kwargs = {"payment_url": {"read_only": True}}

