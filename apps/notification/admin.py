from django.contrib import admin

from apps.common.mixins import TabbedTranslationAdmin
from apps.notification.models import Notification, UserNotification


@admin.register(Notification)
class NotificationAdmin(TabbedTranslationAdmin):
    list_display = ("id", "title", "description", "is_for_everyone")
    ordering = ("-created_at",)


@admin.register(UserNotification)
class NotificationUserAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "notification", "is_sent", "sent_at", "is_read")
    ordering = ("-created_at",)
