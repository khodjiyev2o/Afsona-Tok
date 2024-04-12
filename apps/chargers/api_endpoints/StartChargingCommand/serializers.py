from rest_framework import serializers

from apps.chargers.models import ChargeCommand


class StartChargingCommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargeCommand
        fields = ('id', 'connector', 'user_car')
