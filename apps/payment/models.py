from django.db import models
from apps.common.models import BaseModel
from django.utils.translation import gettext_lazy as _


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
    cid = models.CharField(max_length=255, verbose_name=_("Card Id"))
    expire_date = models.CharField(max_length=255, verbose_name=_("Expire Date"))
    is_confirmed = models.BooleanField(default=False, verbose_name=_("Is Confirmed"))
    balance = models.CharField(_('Balance'), null=True, blank=True, max_length=255)
    vendor = models.CharField(_('Vendor'), max_length=32, choices=VendorType.choices, null=True, blank=True)
    processing = models.CharField(_('Processing'), max_length=255, null=True, blank=True)
    bank_id = models.CharField(_('Bank id'), null=True, blank=True)

    objects = models.Manager()

    class Meta:
        db_table = 'UserCard'
        verbose_name = _('UserCard')
        verbose_name_plural = _('UserCards')
        ordering = ('card_number',)

    def __str__(self):
        return self.card_number


class Transaction(BaseModel):
    class StatusType(models.TextChoices):
        PENDING = 'pending', _('Pending')
        ACCEPTED = 'accepted', _('Accepted')
        REJECTED = 'rejected', _('Rejected')

    class PaymentType(models.TextChoices):
        CARD = 'CARD', _('CARD')
        CLICK = 'CLICK', _('CLICK')
        PAYME = 'PAYME', _('PAYME')
        UZUM = 'UZUM', _('UZUM')

    card = models.ForeignKey(UserCard, on_delete=models.PROTECT, related_name='transactions',
                             verbose_name=_('Card id'), null=True, blank=True)
    user = models.ForeignKey("users.User", on_delete=models.PROTECT, related_name='transactions')
    amount = models.DecimalField(_('Amount'), max_digits=10, decimal_places=2)
    status = models.CharField(_('Status'), max_length=32, choices=StatusType.choices)
    remote_id = models.CharField(_('Remote id'), max_length=255, null=True)
    tax_amount = models.DecimalField(_('TAX Amount'), max_digits=10, decimal_places=2, default=0.0, null=True,
                                     blank=True)
    paid_at = models.DateTimeField(verbose_name=_("Paid at"), null=True, blank=True)
    payment_type = models.CharField(_("Payment Type"), choices=PaymentType.choices)

    class Meta:
        db_table = 'Transaction'
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')
        ordering = ('remote_id',)

    def __str__(self):
        return f"{self.payment_type} | {self.id}"

