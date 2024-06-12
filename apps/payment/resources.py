from django.utils.translation import gettext_lazy as _
from import_export import resources, fields, widgets

from apps.payment.models import Transaction as PaymentTransaction


class PaymentTransactionResource(resources.ModelResource):
    card__card_number = fields.Field(
        attribute='get_card_number', readonly=True,
        widget=widgets.CharWidget()
    )

    class Meta:
        model = PaymentTransaction
        export_order = ('id', 'card__card_number', 'user__phone', 'amount', 'payment_type', 'created_at', 'status')
        fields = ('id', 'card__card_number', 'user__phone', 'amount', 'payment_type', 'created_at', 'status')
        name = _("Export Payment Transactions")

    def get_export_headers(self, fields=None):
        return [_("ID"), _("Card Number"), _("Client"), _("Amount"), _("Payment Type"), _("Created At"), _("Status")]

    def get_card_number(self, obj: PaymentTransaction):
        return obj.card.card_number

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('card')
        return queryset
