from django.urls import path

from .api_endpoints import * # noqa

app_name = 'notification'

urlpatterns = [
    path('UserNotificationList/', UserNotificationListView.as_view(), name='notification-list'),
    path('UserNotificationDetail/<int:pk>/', UserNotificationListView.as_view(), name='notification-detail'),
    path('UserNotificationReadAll/', UserNotificationReadAllView.as_view(), name='notification-read-all'),
]