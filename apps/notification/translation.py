from modeltranslation.translator import TranslationOptions, register

from apps.notification.models import Notification


@register(Notification)
class NotificationTranslationOption(TranslationOptions):
    fields = ('title', 'description')
