from django.db import models
from apps.common.models import BaseModel
from apps.users.models import User
from django.utils.translation import gettext_lazy as _


class Notification(BaseModel):
    title = models.CharField(_('Title'), max_length=255)
    description = models.TextField(_('Description'))
    is_for_everyone = models.BooleanField(_("Is for everyone"), default=False)
    users = models.ManyToManyField(User, blank=True, verbose_name=_("Users"))

    class Meta:
        db_table = 'Notification'
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')
        ordering = ('created_at',)

    def __str__(self):
        return self.title


class UserNotification(BaseModel):
    notification = models.ForeignKey(Notification, on_delete=models.PROTECT, related_name='user_notifications',
                                     verbose_name=_('User notification'))
    user = models.ForeignKey('users.User', on_delete=models.PROTECT, related_name='user_notifications',
                             verbose_name=_('User id'))
    is_sent = models.BooleanField(_('Is sent'), default=False)
    is_read = models.BooleanField(_('Is read'), default=False)
    sent_at = models.DateTimeField(_("Sent At"), null=True, blank=True)

    class Meta:
        db_table = 'UserNotification'
        verbose_name = _('UserNotification')
        verbose_name_plural = _('UserNotifications')
        ordering = ('created_at',)

    def __str__(self):
        return getattr(self.notification, 'title')

