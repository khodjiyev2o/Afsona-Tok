from rest_framework import serializers
from apps.common.models import ConnectionType


class ConnectionTypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectionType
        fields = ('id', 'name', 'icon', 'max_voltage', "description", "_type")
