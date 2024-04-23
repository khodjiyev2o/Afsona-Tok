from django.conf import settings
from rest_framework import serializers

from apps.payment.models import UserCard
from apps.payment.payment_types.payme.subscribe.service import PaymeSubscribeCards


class UserCardVerifySerializer(serializers.Serializer):
    token = serializers.CharField(write_only=True)
    code = serializers.CharField(write_only=True)

    def verify_card(self, user_card):
        client = PaymeSubscribeCards(
            base_url=settings.PAYMENT_CREDENTIALS['payme']['subscribe_base_url'],
            paycom_id=settings.PAYMENT_CREDENTIALS['payme']['subscribe_paycom_id']
        )

        response = client.cards_verify(
            verify_code=self.validated_data['code'],
            token=self.validated_data['token']
        )
        if response.get('error', None):
            raise serializers.ValidationError(detail={"payme": response['error']['message']},
                                              code=f"{response['error']['code']}")

        user_card.is_confirmed = True
        user_card.status = UserCard.CardChoices.ACTIVE
        user_card.save(update_fields=['is_confirmed', 'status'])

        return {"success": True}

    def validate(self, attrs):
        user_card = UserCard.objects.filter(
            user=self.context["request"].user, cid=attrs["token"], status=UserCard.CardChoices.PENDING
        ).first()
        if not user_card:
            raise serializers.ValidationError({"card_cid": "Card not found"}, code="card_not_found")
        if user_card.is_confirmed:
            raise serializers.ValidationError({"card_cid": "Card already confirmed"}, code="card_already_confirmed")
        return attrs

