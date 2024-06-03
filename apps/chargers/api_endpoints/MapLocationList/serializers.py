from rest_framework import serializers

from apps.chargers.models import Location


class MapLocationListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ('id', 'latitude', 'longitude')
