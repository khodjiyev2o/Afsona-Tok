from rest_framework import serializers

from apps.chargers.models import ChargeCommand


class StartChargingCommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargeCommand
        fields = ('id', 'connector', 'user_car', 'is_delivered', 'is_limited', 'limited_money')
        read_only_fields = ('id', 'is_delivered')
        write_only_fields = ('is_limited', 'limited_money')
