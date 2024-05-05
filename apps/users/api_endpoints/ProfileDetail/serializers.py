from rest_framework import serializers
from apps.users.models import User
from apps.notification.models import UserNotification


class UserProfileSerializer(serializers.ModelSerializer):
    notification_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("full_name", "photo", "phone", "balance", "date_of_birth", "language", "notification_count")

    def get_notification_count(self, obj):
        return UserNotification.objects.filter(user=obj, is_read=False).count()

