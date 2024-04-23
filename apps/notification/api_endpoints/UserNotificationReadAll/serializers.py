from rest_framework import serializers
from apps.notification.models import UserNotification


class UserNotificationListSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='notification.title')

    class Meta:
        model = UserNotification
        fields = ('id', 'title', 'is_read', 'created_at')
