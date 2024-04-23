from rest_framework.generics import RetrieveAPIView

from apps.notification.api_endpoints.UserNotificationDetail.serializers import UserNotificationDetailSerializer
from apps.notification.models import UserNotification


class UserNotificationDetailView(RetrieveAPIView):
    queryset = UserNotification.objects.filter()
    serializer_class = UserNotificationDetailSerializer

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        return queryset.filter(user_id=self.request.user.id)

    def get_object(self):
        instance = super().get_object()

        if not instance.is_read:
            instance.is_read = True
            instance.save(is_read=True, update_fields=['is_read'])
        return instance


__all__ = ['UserNotificationDetailView']
