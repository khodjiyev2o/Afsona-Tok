from rest_framework import serializers


class CardIdentifySerializer(serializers.Serializer):
    digits = serializers.CharField(max_length=6, required=True)
