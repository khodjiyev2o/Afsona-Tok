from rest_framework import serializers
from apps.notification.models import UserNotification


class UserNotificationDetailSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='notification.title')
    description = serializers.CharField(source='notification.description')

    class Meta:
        model = UserNotification
        fields = ('id', 'title', 'description', 'is_read', 'created_at')
