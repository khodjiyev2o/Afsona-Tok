from django.utils import timezone
from celery import shared_task

from apps.chargers.models import ChargeCommand, ChargingTransaction
from apps.chargers.utils import generate_id_tag


@shared_task
def send_remote_stop_command_to_ocpp_service(transaction_id: int):
    transaction = ChargingTransaction.objects.get(pk=transaction_id)

    command: ChargeCommand = ChargeCommand.objects.create(
        initiator=ChargeCommand.Initiator.SYSTEM,
        user_id=transaction.user_id,
        connector_id=transaction.connector_id,
        user_car=transaction.user_car,
        command=ChargeCommand.Commands.REMOTE_STOP_TRANSACTION,
        id_tag=generate_id_tag()
    )

    is_delivered = command.send_command_stop_to_ocpp_service(transaction.id)
    command.is_delivered = is_delivered
    command.delivered_at = timezone.now()
    command.save(update_fields=['is_delivered', 'delivered_at'])

    return str(dict(command=command.id, is_delivered=is_delivered, delivered_at=command.delivered_at))
