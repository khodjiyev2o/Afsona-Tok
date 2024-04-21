from rest_framework import serializers
from apps.common.models import MainSettings


class MainSettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = MainSettings
        fields = (
            'price',
            'user_minimum_balance',
            'ios_version',
            'android_version',
            'help_phone_number',
            'help_email',
            'help_telegram_link'
        )
