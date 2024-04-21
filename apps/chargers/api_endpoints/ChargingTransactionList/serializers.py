from rest_framework import serializers
from apps.chargers.models import ChargingTransaction
from apps.common.models import UserCar


class CarSerializer(serializers.ModelSerializer):
    model_name = serializers.CharField(source='model.name')
    manufacturer_name = serializers.CharField(source='model.manufacturer.name')

    class Meta:
        model = UserCar
        fields = ('id', 'manufacturer_name', 'model_name')


class ChargingTransactionListSerializer(serializers.ModelSerializer):
    location_name = serializers.CharField(source='connector.charge_point.location.name')
    car = CarSerializer(source='user_car')

    class Meta:
        model = ChargingTransaction
        fields = ('id', 'location_name', 'created_at', 'total_price', 'car')
