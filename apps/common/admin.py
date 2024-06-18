from django.contrib import admin
from django.db.models import Count
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from apps.chargers.models import Location
from apps.common import models


@admin.register(models.StaticPage)
class StaticPageAdmin(admin.ModelAdmin):
    list_display = (
        "title",
    )
    list_display_links = ("title",)
    search_fields = ("title", "content")


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
        if obj.icon:
            try:
                obj
            except Exception:
                return "(No image)"

            return mark_safe(
                '<img src="{0}" width="100" height="100" style="object-fit:contain" />'.format(
                    obj.icon.url
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


@admin.register(models.MainSettings)
class MainSettingsAdmin(admin.ModelAdmin):
    list_display = ('user_minimum_balance', 'ios_version', 'android_version')

    def has_add_permission(self, request):
        if self.model.objects.count() > 0:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(models.AppealTypeList)
class AppealTypeListAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(models.UserAppeal)
class UserAppealAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name')
    search_fields = ('name', 'user__phone_number')


class LocationInline(admin.TabularInline):
    model = Location
    extra = 0
    can_delete = False
    show_change_link = True
    fields = ('name', 'address', 'created_at')
    readonly_fields = ('name', 'address', 'created_at')

    def has_add_permission(self, request, obj):
        return False


@admin.register(models.District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'region', 'get_location_count')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    search_help_text = _("Search by name")
    inlines = (LocationInline,)
    list_filter = ('region',)
    autocomplete_fields = ('region',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(locations_count=Count('location'))
        return queryset

    def get_location_count(self, obj):
        return obj.location_set.count()

    get_location_count.short_description = _('Location Count')
    get_location_count.admin_order_field = 'locations_count'


class DistrictsInline(admin.TabularInline):
    model = models.District
    extra = 0
    can_delete = False
    show_change_link = True
    readonly_fields = ('name', 'created_at')

    def has_add_permission(self, request, obj):
        return False


@admin.register(models.Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'country', "get_district_count")
    list_filter = ('country',)
    list_display_links = ('id', 'name')
    search_fields = ("name",)
    search_help_text = _("Search by Region and Country's name")
    autocomplete_fields = ('country',)
    inlines = (DistrictsInline,)
    ordering = ('name',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(district_count=Count('districts'))
        return queryset

    def get_district_count(self, obj: models.District.objects):
        return obj.districts.count()

    get_district_count.short_description = _("Regions Count")
    get_district_count.admin_order_field = 'district_count'


class RegionsInline(admin.TabularInline):
    model = models.Region
    extra = 0
    can_delete = False
    show_change_link = True
    readonly_fields = ('name', 'created_at')

    def has_add_permission(self, request, obj):
        return False


@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'ico_code', 'created_at')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    search_help_text = _("Search by name")
    date_hierarchy = 'created_at'
    ordering = ('name',)
    inlines = (RegionsInline,)


@admin.register(models.SavedLocation)
class SavedLocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'location')
    search_fields = ('user__phone_number', 'location__name')
    autocomplete_fields = ('user', 'location')

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False
