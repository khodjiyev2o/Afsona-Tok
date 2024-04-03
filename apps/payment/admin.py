from django.contrib import admin
from django.utils.safestring import mark_safe
from apps.payment import models


@admin.register(models.UserCard)
class UserCardAdmin(admin.ModelAdmin):
    search_fields = ("id",)
    list_display = (
        "id",
        "user",
        "status",
        "card_number",
        "balance",
        "vendor",
        "processing",
        "bank_id",
    )
    list_filter = ("created_at",)
    list_per_page = 20
    ordering = ("-created_at",)

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(models.Transaction)
class TransactionModel(admin.ModelAdmin):
    search_fields = ("id",)
    list_display = (
        "id",
        "card",
        "user",
        "amount",
        "remote_id",
        "colored_status",
    )
    list_filter = ("created_at",)
    list_per_page = 20
    ordering = ("-created_at",)

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def colored_status(self, obj):
        colors = {
            models.Transaction.StatusType.PENDING: "gray",
            models.Transaction.StatusType.ACCEPTED: "green",
            models.Transaction.StatusType.REJECTED: "red",
        }
        if obj.status:
            return mark_safe(f'<span style="color:{colors[obj.status]}"><b>{obj.get_status_display()}</b></span>')
        return f"{obj.status} --- null"

    colored_status.short_description = "Status"  # type: ignore
