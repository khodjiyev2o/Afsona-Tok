from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ChargersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.chargers'
    verbose_name = _('Chargers')

    def ready(self):
        import apps.chargers.signals  # noqa