from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, AllTransactionHistory
from apps.chargers.proxy_models import FinishedChargingTransactionProxy
from apps.payment.models import Transaction
from django.urls import reverse_lazy


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("phone", "password")}),
        (_("Personal info"), {"fields": ("full_name", "date_of_birth", "photo", "balance"
                                         )}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone", "password1", "password2"),
            },
        ),
    )
    list_display = ("id", "full_name", "phone", "is_staff", "balance", "created_at")
    list_display_links = ("id", "full_name")
    list_filter = ("is_superuser", "is_staff", "created_at", "created_at")
    search_fields = (
        "id",
        "full_name",
        "phone",
    )
    readonly_fields = ("id", "created_at", "balance")
    exclude = ("last_login", "updated_at", "password", "is_active", "email")
    ordering = ("-created_at",)


@admin.register(AllTransactionHistory)
class AllTransactionHistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'action', "created_at", "get_more_information"]
    list_filter = ['created_at', 'user', 'action']
    autocomplete_fields = ['user']
    search_fields = ['user__phone', 'action']
    date_hierarchy = 'created_at'

    def get_more_information(self, obj: AllTransactionHistory):
        model_mapping = {
            AllTransactionHistory.Actions.CHARGE.value: FinishedChargingTransactionProxy,
            AllTransactionHistory.Actions.PAYMENT.value: Transaction,
        }
        model = model_mapping.get(obj.action, None)
        if not model:
            return _("No more information available")

        url = reverse_lazy(f"admin:{model._meta.app_label}_{model._meta.model_name}_change", args=[obj.id])
        return mark_safe(f'<a target="_blank" href="{url}">{_("More info")}</a>')

    get_more_information.short_description = _("More info")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
