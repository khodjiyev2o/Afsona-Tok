from rest_framework import serializers

from apps.chargers.models import ChargeCommand


class CommandCallbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargeCommand
        fields = ('status',)

