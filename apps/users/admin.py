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
    readonly_fields = ("id", "created_at")
    exclude = ("last_login", "updated_at", "password", "is_active", "email")
    ordering = ("-created_at",)
