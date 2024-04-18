from rest_framework import serializers

from apps.common.api_endpoints.ConnectionTypeList.serializers import ConnectionTypeListSerializer
from apps.common.models import UserCar, ConnectionType, Instruction


class UserCarConnectionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectionType
        fields = ('id', 'name', 'icon', "_type")


class UserCarListSerializer(serializers.ModelSerializer):
    manufacturer = serializers.CharField(source='manufacturer.name')
    model = serializers.CharField(source='model.name')
    connector_type = ConnectionTypeListSerializer(many=True)

    class Meta:
        model = UserCar
        fields = (
            'id',
            'vin',
            'state_number',
            'state_number_type',
            'manufacturer',
            'model',
            'connector_type',
        )


class InstructionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instruction
        fields = ('id', 'text', 'image')
