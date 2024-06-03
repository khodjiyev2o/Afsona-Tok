from rest_framework import serializers

from apps.common.models import UserCar


class UserCarEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserCar
        fields = (
            "vin",
            "state_number",
            "state_number_type",
            "model"
        )
