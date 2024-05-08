import json
from decimal import Decimal

from django.contrib import admin
from django.db.models import Count
from django.utils.translation import gettext_lazy as _
from import_export.admin import ExportActionMixin

from apps.chargers.models import ChargePoint, Connector, Location, ChargeCommand, OCPPServiceRequestResponseLogs
from apps.chargers.proxy_models import InProgressChargingTransactionProxy, FinishedChargingTransactionProxy
from apps.chargers.resources import FinishedChargingTransactionProxyResource
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


@admin.register(ChargeCommand)
class ChargeCommandAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'user_car', 'connector', 'created_at', 'status', 'id_tag')
    list_filter = ('status', 'user', 'connector')
    search_help_text = _("Search by user's username and user car's plate")


@admin.register(InProgressChargingTransactionProxy)
class InProgressChargingTransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'connector', 'created_at', 'consumed_kwh', 'duration_in_minute')
    list_filter = ('user', 'connector', 'start_reason')

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        result = super().has_delete_permission(request, obj)
        return result and True

    def has_delete_permission(self, request, obj=None):
        result = super().has_delete_permission(request, obj)
        return result and True


@admin.register(FinishedChargingTransactionProxy)
class FinishedChargingTransactionAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_classes = (FinishedChargingTransactionProxyResource,)
    list_display = (
        'id', 'user', 'connector',
        'created_at', 'end_time', 'meter_used',
        'duration_in_minute', 'total_price'
    )
    list_filter = ('user', 'connector__charge_point', 'start_reason', 'stop_reason')
    search_help_text = _("Search by user's username and user car's plate")
    date_hierarchy = 'created_at'

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        result = super().has_delete_permission(request, obj)
        return result and True

    def get_export_filename(self, request, queryset, file_format):
        """ Custom export filename for FinishedChargingTransactionProxy """
        return super().get_export_filename(request, queryset, file_format)


@admin.register(OCPPServiceRequestResponseLogs)
class OCPPServiceRequestResponseLogAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site, *args, **kwargs):
        super().__init__(model, admin_site, )
        self.request_body_formatting_mapping = {
            "StartTransaction": self.__format_start_transaction,
            "MeterValues": self.__format_meter_values,
            "StopTransaction": self.__format_stop_transaction,
            "StatusNotification": self.__format_status_notification
        }

    list_display = ('id', 'charger_id', 'request_action', 'format_request_body', 'response_body', 'created_at')
    list_filter = ('request_action', 'charger_id')
    search_fields = ('charger_id', 'request_action')
    search_help_text = _("Search by charger_id and request_action")
    date_hierarchy = 'created_at'

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def format_request_body(self, obj):
        format_method = self.request_body_formatting_mapping.get(obj.request_action)
        if callable(format_method):
            return format_method(json.loads(obj.request_body.replace("'", "\"")))
        return obj.request_body

    format_request_body.short_description = _("Request Body")

    @staticmethod
    def __format_meter_values(data: dict) -> dict:
        meter_values = data.get('meter_value', [{}])[0].get('sampled_value', [])

        result_data = {'transaction_id': data.get('transaction_id')}
        measurand_list = ['Energy.Active.Import.Register', 'SoC']
        for meter_value in meter_values:
            measurand = meter_value.get("measurand")
            value = meter_value.get("value")
            if measurand not in measurand_list:
                continue
            result_data[measurand] = value

        return result_data

    @staticmethod
    def __format_start_transaction(data: dict) -> dict:
        data.__delitem__("meter_start")
        data.__delitem__("reservation_id")
        data.__delitem__("timestamp")

        cash_mode = True if data.get('id_tag') == "" else False
        data.setdefault("cash_mode", cash_mode)
        return data

    @staticmethod
    def __format_stop_transaction(data: dict) -> dict:
        transaction_id = data.get("transaction_id")
        meter_stop = data.get("meter_stop")
        reason = data.get('reason')

        return {
            "transaction_id": transaction_id,
            "meter_stop": meter_stop,
            "reason": reason,
        }

    @staticmethod
    def __format_status_notification(data: dict) -> dict:
        connector_id = data.get("connector_id")
        connector_status = data.get("status")
        error_code = data.get("error_code")

        return {
            "connector_id": connector_id,
            "status": connector_status,
            "error_code": error_code
        }
