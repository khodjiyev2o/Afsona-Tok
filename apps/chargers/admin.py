from django.contrib import admin
from django.db.models import Count
from django.utils.translation import gettext_lazy as _

from apps.chargers.models import ChargePoint, Connector, Location, ChargingTransaction

from apps.common.models import ConnectionType


class ChargePointInline(admin.TabularInline):
    model = ChargePoint
    extra = 0
    can_delete = False
    add_form_template = None
    show_change_link = True
    fields = ('name', 'last_heartbeat', 'is_connected', 'is_visible_in_mobile')
    readonly_fields = ('name', 'charger_id', 'last_heartbeat', 'is_connected')


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'district', 'get_charge_points_count')
    list_display_links = ('id', 'name')
    list_filter = ('district',)
    search_fields = ('name', 'address')
    search_help_text = _("Search by name and address")
    inlines = (ChargePointInline,)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(charge_points_count=Count('chargers'))
        return queryset

    def get_charge_points_count(self, obj):
        return obj.chargers.count()

    get_charge_points_count.short_description = _("Charge Points Count")
    get_charge_points_count.admin_order_field = 'charge_points_count'
    get_charge_points_count.empty_value_display = '0'


class ConnectorInline(admin.StackedInline):
    model = Connector
    extra = 0
    can_delete = False
    show_change_link = True

    def has_add_permission(self, request, obj):
        return False


@admin.register(ChargePoint)
class ChargePointAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location', 'charger_id', 'is_connected')
    list_display_links = ('id', 'name')
    list_filter = ('location', 'charger_id', 'is_connected')
    search_fields = ('name', 'charger_id')
    search_help_text = _("Search by name and charger_id")
    inlines = (ConnectorInline,)
    readonly_fields = ('last_boot_notification', 'last_heartbeat', 'is_connected')


@admin.register(Connector)
class ConnectorAdmin(admin.ModelAdmin):
    list_display = ('id', 'charge_point', 'connector_id', 'status', 'name', 'last_status_reason')
    list_filter = ('status', 'charge_point__charger_id', 'standard')
    search_fields = ('charge_point__name', 'charge_point__charger_id')
    search_help_text = _("Search by charge point's name and charger_id")
    autocomplete_fields = ('charge_point', 'standard')
    readonly_fields = ('last_status_reason',)


@admin.register(ConnectionType)
class ConnectionTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', '_type', 'get_linked_connector_count', 'get_linked_cars_count')
    search_fields = ('name',)
    search_help_text = _("Search by name")

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            connector_count=Count('connector'),
            car_count=Count('car_connector_types'),
        )
        return queryset

    def get_linked_connector_count(self, obj):
        return obj.connector_set.count()

    get_linked_connector_count.short_description = _("Linked Connector Count")
    get_linked_connector_count.admin_order_field = 'connector_count'

    def get_linked_cars_count(self, obj):
        return obj.car_connector_types.count()

    get_linked_cars_count.short_description = _("Linked Cars Count")
    get_linked_cars_count.admin_order_field = 'car_count'


@admin.register(ChargingTransaction)
class ChargingTransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'user_car', 'connector', 'created_at', 'end_time', 'status')
    list_filter = ('status', 'user', 'connector')
    search_help_text = _("Search by user's username and user car's plate")
