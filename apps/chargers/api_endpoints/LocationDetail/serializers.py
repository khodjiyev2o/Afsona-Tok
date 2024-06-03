from decimal import Decimal
from math import radians, sin, cos, sqrt, atan2

from rest_framework import serializers

from apps.chargers.models import Location, ChargePoint, Connector
from apps.common.models import ConnectionType


class ConnectionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectionType
        fields = ('id', 'name', 'icon', 'max_voltage', '_type')


class ConnectorListSerializer(serializers.ModelSerializer):
    standard = ConnectionTypeSerializer()

    class Meta:
        model = Connector
        fields = ('id', 'name', 'status', 'standard')


class ChargersListSerializer(serializers.ModelSerializer):
    connectors = ConnectorListSerializer(many=True)

    class Meta:
        model = ChargePoint
        fields = ('id', 'name', 'charger_id', 'is_connected', 'max_electric_power', 'connectors')


class LocationDetailSerializer(serializers.ModelSerializer):
    distance = serializers.SerializerMethodField()
    chargers_count = serializers.SerializerMethodField()
    district = serializers.CharField(source='district.name')
    chargers = ChargersListSerializer(many=True)
    is_favorite = serializers.BooleanField()

    class Meta:
        model = Location
        fields = ('id',
                  'latitude',
                  'longitude',
                  'name',
                  'distance',
                  'address',
                  'chargers_count',
                  'district',
                  'chargers',
                  'is_favorite'
                  )

    def get_chargers_count(self, obj):
        return obj.chargers.count() or 0

    def get_distance(self, obj):
        # Retrieve user's location parameters from the request context or input
        user_latitude = self.context.get('user_latitude')
        user_longitude = self.context.get('user_longitude')

        # Calculate distance using Haversine formula
        if user_latitude is not None and user_longitude is not None:
            user_latitude = Decimal(self.context.get('user_latitude'))
            user_longitude = Decimal(self.context.get('user_longitude'))

            lat1 = radians(user_latitude)
            lon1 = radians(user_longitude)
            lat2 = radians(obj.latitude)
            lon2 = radians(obj.longitude)

            # Haversine formula
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            radius_earth = 6371  # Radius of the Earth in kilometers
            distance_km = radius_earth * c

            return round(distance_km)
        else:
            return None
