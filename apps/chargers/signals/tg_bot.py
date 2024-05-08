import logging
from decimal import Decimal

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.chargers.models import ChargingTransaction
from apps.chargers.ocpp_messages.views.utils import get_price_from_settings
from apps.chargers.tasks import send_report_on_stop_transaction_task

telegram_logger = logging.getLogger('telegram')


@receiver(post_save, sender=ChargingTransaction)
def send_meter_value_to_telegram(sender, instance: ChargingTransaction, **kwargs):
    if instance.status == ChargingTransaction.Status.FINISHED:
        return
    PRICE = get_price_from_settings()
    telegram_logger.info(
        f"""MeterValues:
                Transaction ID: {instance.id}
                Battery Percent: {instance.battery_percent_on_end} %
                Consumed KWh: {instance.consumed_kwh}
                Price until now: {Decimal(str(instance.consumed_kwh)) * PRICE}
        """
    )


@receiver(post_save, sender=ChargingTransaction)
def send_start_transaction_to_telegram(sender, instance, created, **kwargs):
    if created:
        telegram_logger.info(
            f"""Start Transaction:
                    Transaction ID: {instance.id}
                    Meter Start: {instance.meter_on_start} %
                    User Phone: {getattr(instance, "user", "Cash mode")}
            """
        )


@receiver(post_save, sender=ChargingTransaction)
def send_stop_transaction_to_telegram(sender, instance, created, **kwargs):
    if instance.status == ChargingTransaction.Status.FINISHED:
        send_report_on_stop_transaction_task.delay(instance.id)
