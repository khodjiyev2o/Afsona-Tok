from rest_framework import serializers

from apps.chargers.models import ChargingTransaction, ChargeCommand


class StopChargingCommandSerializer(serializers.Serializer):
    transaction = serializers.IntegerField()


class StopChargingCommandResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargeCommand
        fields = ('id', 'connector', 'user_car', 'is_delivered')
        read_only_fields = ('id', 'is_delivered')
