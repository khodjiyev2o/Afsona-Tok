from rest_framework import serializers
from apps.common.models import UserAppeal


class UserAppealCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAppeal
        fields = (
            "name",
        )
