from django.contrib import admin
from django.utils.safestring import mark_safe
from apps.payment import models
from django.utils.translation import gettext_lazy as _


@admin.register(models.UserCard)
class UserCardAdmin(admin.ModelAdmin):
    search_fields = ("id",)
    list_display = (
        "id",
        "user",
        "status",
        "card_number",
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
        "payment_type",
        "remote_id",
        "colored_status",
    )
    list_filter = ("created_at", 'payment_type')
    list_per_page = 20
    ordering = ("-created_at",)
    date_hierarchy = 'created_at'

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def colored_status(self, obj):
        colors = {
            models.Transaction.StatusType.PENDING: "gray",
            models.Transaction.StatusType.ACCEPTED: "green",
            models.Transaction.StatusType.REJECTED: "red",
            models.Transaction.StatusType.CANCELED: "red"
        }
        if obj.status:
            return mark_safe(f'<span style="color:{colors[obj.status]}"><b>{obj.get_status_display()}</b></span>')
        return f"{obj.status} --- null"

    colored_status.short_description = _("Status")
    colored_status.admin_order_field = "status"


@admin.register(models.MerchantRequestLog)
class MerchantRequestLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'payment_type', 'method_type', 'created_at']
    list_filter = ['payment_type', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    search_fields = ['request_body', 'response_body', 'payment_type', 'method_type']

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False
