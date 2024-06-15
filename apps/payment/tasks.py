from celery import shared_task

from apps.notification.models import UserNotification, Notification
from apps.payment.models import Transaction


@shared_task
def send_payment_successful_notification(transaction_id: int):
    transaction = Transaction.objects.get(pk=transaction_id)

    notification = Notification.objects.create(
        title="To'lov muvaffaqiyatli amalga oshirildi",
        title_uz="To'lov muvaffaqiyatli amalga oshirildi",
        title_ru="Оплата прошла успешно",
        title_en="Payment successful",
        description=f"Balansingiz {transaction.amount} so'mga muvaffaqiyatli to'ldirildi",
        description_uz=f"Balansingiz {transaction.amount} so'mga muvaffaqiyatli to'ldirildi",
        description_ru=f"Ваш баланс успешно пополнен на {transaction.amount} сум",
        description_en=f"Your balance was successfully topped up by {transaction.amount} sum",
        is_for_everyone=False,
    )

    notification.users.set([transaction.user])

    transaction.is_notification_sent = True
    transaction.save(update_fields=['is_notification_sent'])

