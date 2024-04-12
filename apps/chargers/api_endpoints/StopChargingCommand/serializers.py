from rest_framework import serializers

from apps.chargers.models import ChargingTransaction


class StopChargingCommandSerializer(serializers.ModelSerializer):
    transaction_id = serializers.IntegerField(source='id')

    class Meta:
        model = ChargingTransaction
        fields = ('transaction_id',)
