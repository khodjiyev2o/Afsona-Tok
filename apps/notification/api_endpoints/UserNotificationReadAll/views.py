from rest_framework.views import APIView
from rest_framework.response import Response

from apps.notification.models import UserNotification


class UserNotificationReadAllView(APIView):

    def post(self, request, *args, **kwargs):
        queryset = UserNotification.objects.all()
        user_notification_list = list(queryset.filter(is_read=False).values_list('id', flat=True))
        queryset.filter(id__in=user_notification_list).update(is_read=True)
        return Response(data={'effected_notification_list': user_notification_list})


__all__ = ['UserNotificationReadAllView']
