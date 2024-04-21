from rest_framework import serializers
from apps.common.models import SavedLocation


class SavedLocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = SavedLocation
        fields = ('location',)
