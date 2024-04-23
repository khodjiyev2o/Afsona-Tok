from decimal import Decimal

from apps.common.models import MainSettings


def get_price_from_settings() -> Decimal:
    instance: MainSettings = MainSettings.objects.last()
    return instance.price
