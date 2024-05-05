from fcm_django.models import FCMDevice
from rest_framework import serializers


class DeviceRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = FCMDevice
        fields = ("device_id", "registration_id", "type")
