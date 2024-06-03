from django.utils.crypto import get_random_string

from apps.chargers.models import ChargeCommand


def generate_id_tag() -> str:
    id_tag = get_random_string(length=20)

    while ChargeCommand.objects.filter(id_tag=id_tag).exists():
        id_tag = get_random_string(length=20)

    return id_tag
