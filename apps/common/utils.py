import sys

import environ
from django.core.cache import cache
from django.conf import settings
from eskiz_sms import EskizSMS

from utils.cache import generate_cache_key, generate_code

env = environ.Env()


def get_message_by_language(language, code):
    messages = {
        "uz": f"Afsona Tok uchun tasdiqlash kodi: {code} LMTI9QwgutH",
        "ru": f"Код подтверждения для Afsona Tok: {code} LMTI9QwgutH",
        "en": f"Verification code for Afsona Tok: {code} LMTI9QwgutH",
    }
    return messages[language]


def send_activation_code_via_sms(phone: str, cache_type: str, session: str, language: str = 'uz'):
    code = generate_code()
    cache.set(generate_cache_key(cache_type, phone, session), code, timeout=120)

    if "test" not in sys.argv:
        eskiz = EskizSMS(email=settings.ESKIZ_EMAIL, password=settings.ESKIZ_PASSWORD)
        eskiz.send_sms(mobile_phone=phone[1:], message=get_message_by_language(language=language, code=code),
                       from_whom="4546", callback_url=None)
