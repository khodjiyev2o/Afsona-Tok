from rest_framework import serializers
from apps.common.models import CarModel


class CarModelListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = ('id', 'name', 'manufacturer')
