from django.utils.translation import gettext_lazy as _
from import_export import resources, fields, widgets

from apps.payment.models import Transaction as PaymentTransaction


class PaymentTransactionResource(resources.ModelResource):
    card_number = fields.Field(readonly=True, widget=widgets.CharWidget())

    class Meta:
        model = PaymentTransaction
        export_order = ('id', 'card_number', 'user__phone', 'amount', 'payment_type', 'created_at', 'status')
        fields = ('id', 'card_number', 'user__phone', 'amount', 'payment_type', 'created_at', 'status')
        name = _("Export Payment Transactions")

    def dehydrate_card_number(self, obj: PaymentTransaction):
        return obj.card.card_number if obj.card else ""

    def get_export_headers(self, fields=None):
        return [_("ID"), _("Card Number"), _("Client"), _("Amount"), _("Payment Type"), _("Created At"), _("Status")]
