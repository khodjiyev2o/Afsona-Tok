from rest_framework import serializers

from apps.chargers.models import Connector
from apps.common.models import ConnectionType


class ConnectionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectionType
        fields = ('id', 'name', 'icon', 'max_voltage', "description", "_type")
        ref_name = "Connection_TypeSerializer"


class ConnectorDetailSerializer(serializers.ModelSerializer):
    standard = ConnectionTypeSerializer()
    charge_point_name = serializers.CharField(source='charge_point.name')

    class Meta:
        model = Connector
        fields = ('id', 'standard', 'status', 'charge_point_name')
