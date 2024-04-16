import logging
from decimal import Decimal

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.chargers.models import ChargingTransaction, Connector
from apps.ocpp_messages.views import PRICE

telegram_logger = logging.getLogger('telegram')
from django.conf import settings

@receiver(post_save, sender=ChargingTransaction)
def sent_logs_to_telegram_bot_while_charging(sender, instance: ChargingTransaction, **kwargs):
    if instance.status == ChargingTransaction.Status.FINISHED:
        return

    total_price_until_now: Decimal = Decimal(str(instance.consumed_kwh)) * settings.CHARGING_PRICE_PER_KWH
    payload = {
        'type': 'send_transaction_data',

        "money": str(round(total_price_until_now, 2)),
        "transaction_id": int(instance.id),
        "battery_percent": int(instance.battery_percent_on_end),
        "consumed_kwh": str(instance.consumed_kwh),
        "status": instance.status,
    }
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(group=f'user_id_{instance.user_id}', message=payload)

    telegram_logger.info(
        f"""MeterValues:
                Transaction ID: {instance.id}
                Battery Percent: {instance.battery_percent_on_end} %
                Consumed KWh: {instance.consumed_kwh}
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
                User Phone: {instance.user}
        """
    )


@receiver(post_save, sender=Connector)
def send_connector_status_to_websocket(sender, instance, **kwargs):
    channel_layer = get_channel_layer()

    payload = {
        'type': 'send_connector_status',
        'status': instance.status,
        'connector_id': instance.id
    }
    async_to_sync(channel_layer.group_send)(group='connectors', message=payload)
