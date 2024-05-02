from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "phone", "is_staff", "balance", "created_at")
    list_display_links = ("id", "full_name")
    list_filter = ("is_superuser", "is_staff", "created_at", "created_at")
    search_fields = (
        "id",
        "full_name",
        "phone",
    )
    readonly_fields = ("id", "created_at", "balance", )
    exclude = ("last_login", "updated_at", "password", "is_active", "email")
