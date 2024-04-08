import logging

from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.chargers.models import ChargingTransaction

telegram_logger = logging.getLogger('telegram')


@receiver(post_save, sender=ChargingTransaction)
def sent_logs_to_telegram_bot_while_charging(sender, instance, **kwargs):
    if instance.status == ChargingTransaction.Status.FINISHED:
        return
    telegram_logger.info(
        f"""MeterValues:
                Transaction ID: {instance.id}
                Battery Percent: {instance.battery_percent_on_end} %
                Consumed KWh: {instance.consumer_kwh}
        """
    )


@receiver(post_save, sender=ChargingTransaction)
def sent_logs_to_telegram_bot_on_start(sender, instance, created, **kwargs):
    if not created:
        return
    telegram_logger.info(
        f"""Start Transaction:
                Transaction ID: {instance.id}
                Meter Start: {instance.meter_on_start} %
                User Phone: {instance.user.phone}
                User Balance: {instance.user.balance}
        """
    )
