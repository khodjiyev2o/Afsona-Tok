from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.payment.models import UserCard
from apps.payment.payment_types.payme.subscribe.service import PaymeSubscribeCards


class CarCreateSerializer(serializers.ModelSerializer):
    response = serializers.DictField(read_only=True)
    token = serializers.CharField(read_only=True)

    class Meta:
        model = UserCard
        fields = (
            "card_number",
            "expire_date",
            "vendor",
            "response",
            "token"
        )
        extra_kwargs = {"card_number": {"write_only": True},
                        "expire_date": {"write_only": True},
                        "vendor": {"write_only": True},
                        }

    def create(self, validated_data):
        user = self.context['request'].user

        client = PaymeSubscribeCards(
            base_url=settings.PAYMENT_CREDENTIALS['payme']['subscribe_base_url'],
            paycom_id=settings.PAYMENT_CREDENTIALS['payme']['subscribe_paycom_id']
        )

        response = client.cards_create(
            number=self.validated_data['card_number'],
            expire=self.validated_data['expire_date'],
            save=True
        )

        if response.get('error', None):
            raise ValidationError(detail={"payme": response['error']['message']}, code=f"{response['error']['code']}")

        instance = UserCard.objects.create(
            status=UserCard.CardChoices.PENDING,
            vendor=self.validated_data['vendor'],
            card_number=self.validated_data['card_number'],
            expire_date=self.validated_data['expire_date'],
            cid=response['result']['card']['token'],
            user=user
        )

        response_2 = client.card_get_verify_code(token=instance.cid)

        return {"token": response['result']['card']['token'], "response": response_2}
