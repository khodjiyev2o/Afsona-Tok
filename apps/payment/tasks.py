from celery import shared_task

from apps.notification.models import UserNotification, Notification
from apps.payment.models import Transaction


@shared_task
def send_payment_successful_notification(transaction_id: int):
    transaction = Transaction.objects.get(pk=transaction_id)

    notification, created = Notification.objects.get_or_create(
        title="Payment successful",
        title_uz="To'lov muvaffaqiyatli amalga oshirildi 🎉🎉🎉",
        title_ru="Оплата прошла успешно 🎉🎉🎉",
        title_en="Payment successful 🎉🎉🎉",
        description="Your payment was successful",
        description_uz=f"Balansingiz {transaction.amount} so'mga muvaffaqiyatli to'ldirildi",
        description_ru=f"Ваш баланс успешно пополнен на {transaction.amount} сум",
        description_en=f"Your balance was successfully topped up by {transaction.amount} sum",
        is_for_everyone=False,
        users=transaction.user,
    )