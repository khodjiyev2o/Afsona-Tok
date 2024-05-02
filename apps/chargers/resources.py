from import_export import resources

from apps.chargers.models import ChargingTransaction


class ChargingTransactionResource(resources.ModelResource):
    class Meta:
        model = ChargingTransaction
        export_order = ("connector__charge_point__charger_id", 'created_at', 'meter_used', 'total_price')
        fields = ('connector__charge_point__charger_id', 'created_at', 'meter_used', 'total_price')
