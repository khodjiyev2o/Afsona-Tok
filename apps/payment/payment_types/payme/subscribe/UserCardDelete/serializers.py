from rest_framework import serializers

from apps.payment.models import UserCard


class UserCardDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCard
        fields = (
            'status',
        )
