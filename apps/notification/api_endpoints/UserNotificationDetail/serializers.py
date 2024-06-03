from rest_framework import serializers

from apps.notification.models import UserNotification


class UserNotificationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNotification
        fields = ('id', 'is_read')
