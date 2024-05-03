from decimal import Decimal

from django.conf import settings
from rest_framework import serializers
from apps.chargers.models import ChargingTransaction, Connector
from apps.common.models import UserCar, ConnectionType


class ConnectionTypeMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectionType
        fields = ('id', 'icon', 'name')


class InProgressConnectorSerializer(serializers.ModelSerializer):
    standard = ConnectionTypeMiniSerializer()

    class Meta:
        model = Connector
        fields = ('id', 'name', 'standard')


class InProgressCarSerializer(serializers.ModelSerializer):
    model_name = serializers.CharField(source='model.name')
    manufacturer_name = serializers.CharField(source='model.manufacturer.name')

    class Meta:
        model = UserCar
        fields = ('id',  'manufacturer_name', 'model_name', 'state_number', 'state_number_type')


class InProgressChargingTransactionListSerializer(serializers.ModelSerializer):
    car = InProgressCarSerializer(source='user_car')
    battery_percent = serializers.IntegerField(source='battery_percent_on_end')
    connector = InProgressConnectorSerializer()
    money = serializers.SerializerMethodField()
    consumed_kwh = serializers.SerializerMethodField()

    class Meta:
        model = ChargingTransaction
        fields = ('id', 'connector', 'car', 'battery_percent', 'money', 'consumed_kwh', 'start_command_id')

    def get_money(self, obj):
        money = Decimal(str(obj.consumed_kwh)) * settings.CHARGING_PRICE_PER_KWH
        # todo i will refactor
        return str(round(money, 2))

    def get_consumed_kwh(self, obj):
        return obj.consumed_kwh
