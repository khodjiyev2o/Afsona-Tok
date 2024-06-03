from decimal import Decimal

import pytz
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.chargers.models import ChargingTransaction, Connector


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
    total_price_until_now: Decimal = Decimal(str(instance.consumed_kwh)) * instance.price_per_kwh
    payload = {
        "type": 'send_meter_values_data',  # method name in the consumer: apps/chargers/consumers.py:36

        "money": str(round(total_price_until_now, 2)),
        "transaction_id": int(instance.id),
        "start_command_id": instance.start_command_id,
        "battery_percent": int(instance.battery_percent_on_end),
        "consumed_kwh": str(instance.consumed_kwh),
        "status": instance.status,
    }
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(group=f'user_id_{instance.user_id}', message=payload)


@receiver(post_save, sender=ChargingTransaction)
def send_stop_transaction_to_websocket(sender, instance: ChargingTransaction, **kwargs):
    if instance.status == ChargingTransaction.Status.FINISHED:
        created_at_iso_format = instance.created_at.astimezone(pytz.timezone(settings.TIME_ZONE)).isoformat()
        payload = {
            "type": "send_transaction_cheque",

            "transaction_id": instance.id,
            "charging_has_started_at": created_at_iso_format,
            "location_name": instance.connector.charge_point.location.name,
            "consumed_kwh": str(instance.consumed_kwh),
            "total_price": str(instance.total_price),
            "charging_duration_in_minute": instance.duration_in_minute,
        }
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(group=f'user_id_{instance.user_id}', message=payload)
