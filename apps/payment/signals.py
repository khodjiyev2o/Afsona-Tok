from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.payment.models import Transaction
from apps.payment.tasks import send_payment_successful_notification


@receiver(post_save, sender=Transaction)
def payment_successful(sender, instance, **kwargs):
    if instance.status == Transaction.StatusType.ACCEPTED and instance.is_notification_sent is False:
        send_payment_successful_notification.delay(instance.id)
