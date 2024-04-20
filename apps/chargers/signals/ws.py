from decimal import Decimal

from django.dispatch import receiver
from django.conf import settings
from apps.chargers.models import ChargingTransaction, Connector
from django.db.models.signals import post_save
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


@receiver(post_save, sender=Connector)
def send_connector_status_to_websocket(sender, instance, **kwargs):
    channel_layer = get_channel_layer()

    payload = {
        'type': 'send_connector_status',  # method name in the consumer: apps/chargers/consumers.py:24
        'status': instance.status,
        'connector_id': instance.id
    }
    async_to_sync(channel_layer.group_send)(group='connectors', message=payload)


@receiver(post_save, sender=ChargingTransaction)
def send_meter_value_to_websocket(sender, instance: ChargingTransaction, **kwargs):
    if instance.status == ChargingTransaction.Status.FINISHED:
        return

    total_price_until_now: Decimal = Decimal(str(instance.consumed_kwh)) * settings.CHARGING_PRICE_PER_KWH
    payload = {
        "type": 'send_meter_values_data',  # method name in the consumer: apps/chargers/consumers.py:36

        "money": str(round(total_price_until_now, 2)),
        "transaction_id": int(instance.id),
        "battery_percent": int(instance.battery_percent_on_end),
        "consumed_kwh": str(instance.consumed_kwh),
        "status": instance.status,
    }
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(group=f'user_id_{instance.user_id}', message=payload)


@receiver(post_save, sender=ChargingTransaction)
def send_stop_transaction_to_websocket(sender, instance: ChargingTransaction, created, **kwargs):
    if instance.status == ChargingTransaction.Status.FINISHED:
        duration_in_minute = (instance.end_time - instance.created_at).total_seconds() // 60

        payload = {
            "type": "send_transaction_cheque",

            "transaction_id": instance.id,
            "charging_has_started_at": instance.created_at.isoformat(),
            "location_name": instance.connector.charge_point.location.name,
            "consumed_kwh": str(instance.consumed_kwh),
            "total_price": str(instance.total_price),
            "charging_duration_in_minute": duration_in_minute,
        }
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(group=f'user_id_{instance.user_id}', message=payload)
