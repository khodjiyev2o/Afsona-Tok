from django.utils.translation import gettext_lazy as _
from import_export import resources

from apps.chargers.proxy_models import FinishedChargingTransactionProxy


class FinishedChargingTransactionProxyResource(resources.ModelResource):
    class Meta:
        model = FinishedChargingTransactionProxy
        export_order = ('id', "connector__charge_point__charger_id", 'created_at', 'meter_used', 'total_price')
        fields = ('id', 'connector__charge_point__charger_id', 'created_at', 'meter_used', 'total_price')
        name = _("Export Charging Transactions")

    def get_export_headers(self, fields=None):
        return [_("ID"), _("Charger ID"), _("Created At"), _("Meter Used"), _("Total Price")]
