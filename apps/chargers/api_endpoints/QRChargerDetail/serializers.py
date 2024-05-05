from rest_framework import serializers

from apps.chargers.models import ChargePoint, Connector
from apps.common.models import ConnectionType


class ConnectionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectionType
        fields = ('id', 'name', 'icon', 'max_voltage', '_type')
        ref_name = 'DeepLinkConnectionTypeSerializer'


class ConnectorListSerializer(serializers.ModelSerializer):
    standard = ConnectionTypeSerializer()

    class Meta:
        model = Connector
        fields = ('id', 'name', 'status', 'standard')
        ref_name = 'DeepLinkConnectorListSerializer'


class ChargersDetailSerializer(serializers.ModelSerializer):
    connectors = ConnectorListSerializer(many=True)

    class Meta:
        model = ChargePoint
        fields = ('id', 'name', 'charger_id', 'is_connected', 'max_electric_power', 'connectors')


