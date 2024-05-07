from rest_framework import generics

from apps.notification.api_endpoints.UserNotificationList.serializers import UserNotificationListSerializer
from apps.notification.models import UserNotification


class UserNotificationListView(generics.ListAPIView):
    queryset = UserNotification.objects.filter()
    serializer_class = UserNotificationListSerializer

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        return queryset.filter(user_id=self.request.user.id).order_by("-created_at")


__all__ = ['UserNotificationListView']
