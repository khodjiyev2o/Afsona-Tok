from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.utils import timezone
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification

from apps.notification.models import Notification as Notif, UserNotification
from apps.users.models import User


@receiver(post_save, sender=Notif)
def create_user_notification_all(sender, instance, created, **kwargs):
    """This works when a notification is for everyone."""
    if created and instance.is_for_everyone:
        message = Message(
            notification=Notification(title=instance.title, body=instance.description),
        )
        notification_users = UserNotification.objects.bulk_create(
            (UserNotification(user_id=user.id, notification_id=instance.id, is_sent=True, sent_at=timezone.now()) for
             user in User.objects.all())
        )
        users_id = [notification_user.user.id for notification_user in notification_users]
        devices = FCMDevice.objects.filter(user__in=users_id)
        response = devices.send_message(message=message)


@receiver(m2m_changed, sender=Notif.users.through)
def create_user_notification(sender, instance, action, **kwargs):
    """This works when a notification is not for everyone."""
    if action == "post_add":
        if instance.is_for_everyone:
            instance.users.clear()
        else:
            notification_users = UserNotification.objects.bulk_create(
                (UserNotification(user_id=user.id, notification_id=instance.id, is_sent=True, sent_at=timezone.now())
                 for user in instance.users.all())
            )

            # Group users by language preference
            user_language_map = {}
            for user in instance.users.all():
                user_language_map.setdefault(user.language, []).append(user.id)

            # Send messages based on user language
            for language, user_ids in user_language_map.items():
                title = getattr(instance, f'title_{language}', instance.title)
                body = getattr(instance, f'description_{language}', instance.description)

                message = Message(
                    notification=Notification(title=title, body=body),
                )
                devices = FCMDevice.objects.filter(user__in=user_ids)
                devices.send_message(message)
