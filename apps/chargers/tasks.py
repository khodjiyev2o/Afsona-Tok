from django.utils import timezone
from celery import shared_task
from telegram.bot import Bot
from django.conf import settings
from apps.chargers.models import ChargeCommand, ChargingTransaction
from apps.chargers.utils import generate_id_tag
import pytz


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

    is_delivered = command.send_command_stop_to_ocpp_service(
        transaction_id=transaction.id, retry=3, timeout=1
    )
    command.is_delivered = is_delivered
    command.delivered_at = timezone.now()
    command.save(update_fields=['is_delivered', 'delivered_at'])

    return str(dict(command=command.id, is_delivered=is_delivered, delivered_at=command.delivered_at))


@shared_task
def send_report_on_stop_transaction_task(transaction_id: int):
    transaction: ChargingTransaction = ChargingTransaction.objects.get(pk=transaction_id)
    bot = Bot(token='6776606012:AAHG0sKQtsfJ-PjDnNhRyw3QDr3mtRPQlM0')

    user = str(transaction.user.phone) if transaction.user else "Naxt pul"

    message = f"""Transaction ID: {transaction.id}
Boshlangan vaqt: {transaction.created_at.astimezone(pytz.timezone(settings.TIME_ZONE)).strftime("%B %d, %Y, %H:%M:%S")}
Davomiyligi: {transaction.end_time - transaction.created_at}
Ishlatilingan kWh: {transaction.meter_used} 
Address : {transaction.connector.charge_point.name} - {transaction.connector.name}
Narxi: {transaction.total_price}
Klient: {user}"""

    bot.send_message(chat_id='-1002102673622', text=message)

    return str(dict(transaction=transaction.id, report_sent=True))
