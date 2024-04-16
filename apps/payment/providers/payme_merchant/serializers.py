from rest_framework import serializers


class PaymeCallbackSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    method = serializers.CharField()
    params = serializers.JSONField()
