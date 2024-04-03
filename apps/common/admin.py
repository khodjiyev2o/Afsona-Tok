from django.contrib import admin
from django.utils.safestring import mark_safe
from apps.common import models


@admin.register(models.FrontendTranslation)
class FrontTranslationAdmin(admin.ModelAdmin):
    list_display = ("id", "key", "text", "created_at", "updated_at")
    list_display_links = ("id", "key")
    list_filter = ("created_at", "updated_at")
    search_fields = ("key", "version")


@admin.register(models.Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "image_preview"]
    search_fields = ["name"]
    list_per_page = 20

    def image_preview(self, obj):
        if obj.file:
            try:
                obj
            except Exception:
                return "(No image)"

            return mark_safe(
                '<img src="{0}" width="100" height="100" style="object-fit:contain" />'.format(
                    obj.file.url
                )
            )
        else:
            return "(No image)"


@admin.register(models.CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "manufacturer"]
    search_fields = ["name"]


@admin.register(models.UserCar)
class UserCarAdmin(admin.ModelAdmin):
    list_display = ["id", "vin", "model", "state_number", "state_number_type", "user"]
    autocomplete_fields = ["model", "user"]
    search_fields = ["vin", "model"]


@admin.register(models.Support)
class SupportAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if self.model.objects.count() > 0:
            return False
        return True

