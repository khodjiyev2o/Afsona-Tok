from django.db import models

from apps.chargers.models import ChargingTransaction


class InProgressChargingTransactionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=ChargingTransaction.Status.IN_PROGRESS)


class FinishedChargingTransactionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=ChargingTransaction.Status.FINISHED)
