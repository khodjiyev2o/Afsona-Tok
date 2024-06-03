import random
import string

from django.core.cache import cache


class CacheTypes:  # noqa
    registration_sms_verification = "login_sms_verification"


def generate_cache_key(type_, *args):
    return f"{type_}{''.join(args)}"


def generate_code():
    return "".join(random.choice(string.digits) for _ in range(6))


def is_code_valid(cache_key, code):
    valid_code = cache.get(cache_key)
    if valid_code != code:
        return False
    return True
