from rest_framework import serializers

from apps.common.models import Manufacturer


class ManufacturerListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Manufacturer
        fields = (
            'id',
            'name',
            'icon',
        )
