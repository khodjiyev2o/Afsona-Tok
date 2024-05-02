from rest_framework import serializers

from apps.payment.models import UserCard


class UserCardListSerializer(serializers.ModelSerializer):
    card_number = serializers.SerializerMethodField()

    class Meta:
        model = UserCard
        fields = (
            'id',
            'card_number',
            'expire_date',
            'vendor'
        )

    def get_card_number(self, obj):
        return f"{obj.card_number[:4]}********{obj.card_number[-2:]}"

