import logging
import os
from decimal import Decimal

from django.db.models.signals import post_save
from django.dispatch import receiver
from telegram.bot import Bot
from telegram.parsemode import ParseMode

from apps.chargers.models import ChargingTransaction, Connector
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


@receiver(post_save, sender=Connector)
def send_stop_transaction_to_telegram(sender, instance, **kwargs):
    if instance.status in [
        Connector.Status.AVAILABLE,
        Connector.Status.PREPARING,
        Connector.Status.CHARGING,
        Connector.Status.FINISHING
    ]:
        return

    token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('ERROR_LOG_CHANNEL_ID')

    Bot(token=token).send_message(
        chat_id=chat_id, parse_mode=ParseMode.HTML,
        text=f"Connector ID: {instance.id} has status: {instance.status}"
    )
