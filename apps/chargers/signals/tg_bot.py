import logging
import os

from django.db.models.signals import post_save
from django.dispatch import receiver
from telegram.bot import Bot
from telegram.parsemode import ParseMode

from apps.chargers.models import ChargingTransaction, Connector
from apps.chargers.tasks import send_report_on_stop_transaction_task, send_user_notification_on_stop_transaction_task

telegram_logger = logging.getLogger('telegram')


@receiver(post_save, sender=ChargingTransaction)
def send_stop_transaction_to_telegram(sender, instance, created, **kwargs):
    if instance.status == ChargingTransaction.Status.FINISHED:
        send_user_notification_on_stop_transaction_task.delay(instance.id)
        send_report_on_stop_transaction_task.delay(instance.id)


@receiver(post_save, sender=Connector)
def send_connector_error_status_to_telegram(sender, instance: Connector, **kwargs):
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
        text=f"Connector {instance.status}: {instance.charge_point} - {instance.name}"
    )
