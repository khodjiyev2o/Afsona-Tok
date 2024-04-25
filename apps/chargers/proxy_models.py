from apps.chargers.managers import InProgressChargingTransactionManager, FinishedChargingTransactionManager
from apps.chargers.models import ChargingTransaction
from django.utils.translation import gettext_lazy as _


class FinishedChargingTransactionProxy(ChargingTransaction):
    objects = FinishedChargingTransactionManager()

    class Meta:
        proxy = True
        verbose_name = _('Finished Charging Transaction')
        verbose_name_plural = _('Finished Charging Transactions')

    def __init__(self, *args, **kwargs):
        """ Change the verbose names of the fields """
        super().__init__(*args, **kwargs)
        self._meta.get_field('created_at').verbose_name = _("Start Time")
        self._meta.get_field('meter_used').verbose_name = _("Consumed kWh")


class InProgressChargingTransactionProxy(ChargingTransaction):
    objects = InProgressChargingTransactionManager()

    class Meta:
        proxy = True
        verbose_name = _('In Progress Charging Transaction')
        verbose_name_plural = _('In Progress Charging Transactions')

    def __init__(self, *args, **kwargs):
        """ Change the verbose names of the fields """
        super().__init__(*args, **kwargs)
        self._meta.get_field('created_at').verbose_name = _("Start Time")
