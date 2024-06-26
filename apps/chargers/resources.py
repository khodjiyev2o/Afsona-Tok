from django.utils.translation import gettext_lazy as _
from import_export import resources, fields

from apps.chargers.proxy_models import FinishedChargingTransactionProxy


class FinishedChargingTransactionProxyResource(resources.ModelResource):
    cash_mode = fields.Field(column_name=_("Cash Mode"))

    class Meta:
        model = FinishedChargingTransactionProxy
        export_order = ('id', "connector__charge_point__name", 'created_at', 'cash_mode', 'user__phone', 'meter_used', 'total_price')
        fields = ('id', 'connector__charge_point__name', 'created_at', 'cash_mode', 'user__phone', 'meter_used', 'total_price',)
        name = _("Export Charging Transactions")

    def dehydrate_cash_mode(self, obj):
        return obj.user is None

    def get_export_headers(self, fields=None):
        return [_("ID"), _("Charger Name"), _("Created At"),  _("Cash Mode"), _("Phone"), _("Meter Used"), _("Total Price")]
