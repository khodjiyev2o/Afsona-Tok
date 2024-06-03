import sys

import environ
from django.conf import settings
from django.core.cache import cache
from eskiz_sms import EskizSMS

from utils.cache import generate_cache_key, generate_code

env = environ.Env()


def get_message_by_language(language, code):
    messages = {
        "uz": f"Afsona Tok ilova ga ro‘yxatdan o‘tish uchun tasdiqlash kodi: {code} LMTl9QwgutH",
        "ru": f"Код подтверждения регистрации в приложении Афсона Ток: {code} LMTl9QwgutH",
        "en": f"Confirmation code for registration to Afsona Tok application: {code} LMTl9QwgutH",
    }
    return messages[language]


def send_activation_code_via_sms(phone: str, cache_type: str, session: str, language: str = 'uz'):
    code = generate_code()
    cache.set(generate_cache_key(cache_type, phone, session), code, timeout=120)

    if "test" not in sys.argv:
        eskiz = EskizSMS(email=settings.ESKIZ_EMAIL, password=settings.ESKIZ_PASSWORD)
        eskiz.send_sms(mobile_phone=phone[1:], message=get_message_by_language(language=language, code=code),
                       from_whom="4546", callback_url=None)
