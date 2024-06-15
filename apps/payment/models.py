import base64

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel
from .tasks import send_payment_successful_notification


class UserCard(BaseModel):
    class CardChoices(models.TextChoices):
        PENDING = ('pending', _('Pending'))
        ACTIVE = ('active', _('Active'))
        DELETED = ('deleted', _('Deleted'))

    class VendorType(models.TextChoices):
        HUMO = ('humo', _('Humo'))
        UZCARD = ('uzcard', _('Uzcard'))

    status = models.CharField(_('Status'), max_length=16, choices=CardChoices.choices)
    user = models.ForeignKey('users.User', on_delete=models.PROTECT, related_name='user_cards')
    card_number = models.CharField(_('Card number'), max_length=32)
    cid = models.TextField(verbose_name=_("Card Id"))
    expire_date = models.CharField(max_length=255, verbose_name=_("Expire Date"))
    is_confirmed = models.BooleanField(default=False, verbose_name=_("Is Confirmed"))
    vendor = models.CharField(_('Vendor'), max_length=32, choices=VendorType.choices, null=True, blank=True)

    objects = models.Manager()

    class Meta:
        db_table = 'UserCard'
        verbose_name = _('UserCard')
        verbose_name_plural = _('UserCards')
        ordering = ('card_number',)
        unique_together = ['user', 'card_number', 'expire_date', 'status', 'cid']

    def __str__(self):
        return self.card_number


class Transaction(BaseModel):
    class StatusType(models.TextChoices):
        PENDING = 'pending', _('Pending')
        ACCEPTED = 'accepted', _('Accepted')
        REJECTED = 'rejected', _('Rejected')
        CANCELED = 'canceled', _('Canceled')

    class PaymentType(models.TextChoices):
        CARD = 'CARD', _('CARD')
        CLICK = 'CLICK', _('CLICK')
        PAYME = 'PAYME', _('PAYME')
        UZUM = 'UZUM', _('UZUM')

    card = models.ForeignKey(UserCard, on_delete=models.PROTECT, related_name='transactions',
                             verbose_name=_('Card id'), null=True, blank=True)
    user = models.ForeignKey("users.User", on_delete=models.PROTECT, related_name='transactions')
    amount = models.DecimalField(_('Amount'), max_digits=10, decimal_places=2)
    status = models.CharField(_('Status'), max_length=32, choices=StatusType.choices, default=StatusType.PENDING)
    remote_id = models.CharField(_('Remote id'), max_length=255, null=True, blank=True)
    tax_amount = models.DecimalField(_('TAX Amount'), max_digits=10, decimal_places=2, default=0.0, null=True,
                                     blank=True)
    paid_at = models.DateTimeField(verbose_name=_("Paid at"), null=True, blank=True)
    canceled_at = models.DateTimeField(verbose_name=_("Canceled at"), null=True, blank=True)
    payment_type = models.CharField(_("Payment Type"), choices=PaymentType.choices)
    extra = models.JSONField(_('Extra'), null=True, blank=True)
    is_notification_sent = models.BooleanField(_('Is notification sent'), default=False)

    class Meta:
        db_table = 'Transaction'
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')
        ordering = ('remote_id',)

    def __str__(self):
        return f"{self.payment_type} | {self.id}"

    def success_process(self):
        self.user.balance += self.amount
        self.user.save(update_fields=['balance'])

        self.status = self.StatusType.ACCEPTED
        self.save(update_fields=['status'])
        send_payment_successful_notification.delay(self.id)

    def cancel_process(self):
        self.user.balance -= self.amount
        self.user.save(update_fields=['balance'])

        self.status = self.StatusType.CANCELED
        self.save(update_fields=['status'])

    @property
    def payment_url(self):
        payment_url = ""
        if self.payment_type == Transaction.PaymentType.PAYME:
            merchant_id = settings.PAYMENT_CREDENTIALS['payme']['merchant_id']
            params = f"m={merchant_id};ac.order_id={self.id};a={self.amount * 100};"
            encode_params = base64.b64encode(params.encode("utf-8"))
            encode_params = str(encode_params, "utf-8")
            payment_url = f"{settings.PAYMENT_CREDENTIALS['payme']['callback_url']}/{encode_params}"

        elif self.payment_type == Transaction.PaymentType.CLICK:
            merchant_id = settings.PAYMENT_CREDENTIALS['click']["merchant_id"]
            service_id = settings.PAYMENT_CREDENTIALS['click']["merchant_service_id"]
            params = (
                f"?service_id={service_id}&merchant_id={merchant_id}&"
                f"amount={self.amount}&transaction_param={self.id}"
            )
            payment_url = f"{settings.PAYMENT_CREDENTIALS['click']['callback_url']}/{params}"

        return payment_url


class MerchantRequestLog(BaseModel):
    payment_type = models.CharField(max_length=50, verbose_name=_("Payment type"), choices=Transaction.PaymentType.choices)
    method_type = models.CharField(max_length=255, verbose_name=255, null=True, blank=True)
    request_headers = models.TextField(verbose_name=_("Request Headers"), null=True)
    request_body = models.TextField(verbose_name=_("Request Body"), null=True)

    response_headers = models.TextField(verbose_name=_("Response Headers"), null=True)
    response_body = models.TextField(verbose_name=_("Response Body"), null=True)
    response_status_code = models.PositiveSmallIntegerField(verbose_name=_("Response status code"), null=True)
