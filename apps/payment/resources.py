from django.utils.translation import gettext_lazy as _
from import_export import resources

from apps.payment.models import Transaction as PaymentTransaction


class PaymentTransactionResource(resources.ModelResource):
    class Meta:
        model = PaymentTransaction
        export_order = ('id', 'card', 'user__phone', 'amount', 'payment_type', 'created_at', 'status')
        fields = ('id', 'card', 'user__phone', 'amount', 'payment_type', 'created_at', 'status')
        name = _("Export Payment Transactions")

    def get_export_headers(self, fields=None):
        return [_("ID"), _("Card Number"), _("Client"), _("Amount"), _("Payment Type"), _("Created At"), _("Status")]
