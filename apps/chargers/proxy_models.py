from apps.chargers.managers import InProgressChargingTransactionManager, FinishedChargingTransactionManager
from apps.chargers.models import ChargingTransaction
from django.utils.translation import gettext_lazy as _


class FinishedChargingTransactionProxy(ChargingTransaction):
    objects = FinishedChargingTransactionManager()

    class Meta:
        proxy = True
        verbose_name = _('Finished Charging Transaction')
        verbose_name_plural = _('Finished Charging Transactions')


class InProgressChargingTransactionProxy(ChargingTransaction):
    objects = InProgressChargingTransactionManager()

    class Meta:
        proxy = True
        verbose_name = _('In Progress Charging Transaction')
        verbose_name_plural = _('In Progress Charging Transactions')
