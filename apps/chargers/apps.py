from django.apps import AppConfig


class ChargersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.chargers'

    def ready(self):
        import apps.chargers.signals # noqa