from django.urls import path

from .api_endpoints import *  # noqa

app_name = 'notification'

urlpatterns = [
    path('UserNotificationList/', UserNotificationListView.as_view(), name='notification-list'),
    path('UserNotificationDetail/<int:pk>/', UserNotificationDetailView.as_view(), name='notification-detail'),
    path('UserNotificationReadAll/', UserNotificationReadAllView.as_view(), name='notification-read-all'),
    path("device/register/", DeviceRegisterView.as_view(), name="device-register"),
]