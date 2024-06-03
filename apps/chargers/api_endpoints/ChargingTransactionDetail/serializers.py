from rest_framework import serializers

from apps.chargers.models import ChargingTransaction


class ChargingTransactionDetailSerializer(serializers.ModelSerializer):
    location_name = serializers.CharField(source='connector.charge_point.location.name')

    class Meta:
        model = ChargingTransaction
        fields = ('id', 'created_at', 'location_name', 'meter_used', 'duration_in_minute', 'total_price')
