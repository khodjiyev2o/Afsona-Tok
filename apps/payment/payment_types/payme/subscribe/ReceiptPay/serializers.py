from django.conf import settings

from rest_framework import serializers
from rest_framework.serializers import ValidationError

from apps.payment.models import UserCard, Transaction

from apps.payment.payment_types.payme.subscribe.service import PaymeSubscribeReceipts


class ReceiptCreateAndPaySerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = (
            'amount',
            'card',
            'status',
        )
        extra_kwargs = {"amount": {"write_only": True}, "card": {"write_only": True}, "status": {"read_only": True}}

    def validate(self, attrs):
        if attrs['amount'] < 10000:
            raise serializers.ValidationError({"amount": "Amount should be 10000"}, code="not_enough")

        user_card = UserCard.objects.filter(
            user=self.context["request"].user, id=attrs["card"].id, status=UserCard.CardChoices.ACTIVE
        ).first()
        if not user_card:
            raise serializers.ValidationError({"card_cid": "Card not found"}, code="card_not_found")
        if not user_card.is_confirmed:
            raise serializers.ValidationError({"card_cid": "Card not confirmed"}, code="card_not_confirmed")
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user

        client = PaymeSubscribeReceipts(
            base_url=settings.PAYMENT_CREDENTIALS['payme']['subscribe_base_url'],
            paycom_id=settings.PAYMENT_CREDENTIALS['payme']['subscribe_paycom_id'],
            paycom_key=settings.PAYMENT_CREDENTIALS['payme']['credential_key']
        )
        transaction = Transaction.objects.create(
            user=user, card=self.validated_data['card'], amount=self.validated_data['amount']
        )

        response = client.receipts_create(
            amount=int(transaction.amount * 100),
            order_id=f"{transaction.id}",
        )

        if response.get('error', None):
            raise ValidationError(detail={"payme": response['error']['message']}, code=f"{response['error']['code']}")

        response2 = client.receipts_pay(
            invoice_id=response['result']['receipt']['_id'],
            token=self.validated_data['card'].cid,
        )
        print("res2", response2)

        if response2.get('error', None):
            raise ValidationError(detail={"payme": response2['error']['message']}, code=f"{response2['error']['code']}")

        return 0
