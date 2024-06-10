import os
from datetime import timedelta
from pathlib import Path

import environ
import sentry_sdk
from django.utils.translation import gettext_lazy as _
from firebase_admin import initialize_app
from import_export.formats.base_formats import XLSX
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.fastapi import FastApiIntegration

from core.jazzmin_conf import *  # noqa
from utils.sentry_tg_bot import before_send_trigger

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# READING ENV
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, ".env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition
DJANGO_APPS = [
    "daphne",  # should add to the beginning
    "jazzmin",
    'rosetta',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize"
]

CUSTOM_APPS = [
    "apps.common",
    "apps.users",
    "apps.chargers",
    "apps.notification",
    "apps.payment"
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "ckeditor",
    "ckeditor_uploader",
    "rest_framework_simplejwt",
    "drf_yasg",
    "corsheaders",
    "modeltranslation",
    "fcm_django",
    "captcha",
    "channels",
    "import_export"
]

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter"
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "EXCEPTION_HANDLER": "utils.exception_handler.custom_exception_handler",
    "PAGE_SIZE": 10,
}

INSTALLED_APPS = DJANGO_APPS + CUSTOM_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"
AUTH_USER_MODEL = "users.User"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.dashboard"
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"
ASGI_APPLICATION = "core.asgi.application"

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": env.str("DB_ENGINE"),
        "NAME": env.str("DB_NAME"),
        "USER": env.str("DB_USER"),
        "PASSWORD": env.get_value("DB_PASSWORD"),
        "HOST": env.str("DB_HOST"),
        "PORT": env.str("DB_PORT"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en'
TIME_ZONE = "Asia/Tashkent"

USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"
STATICFILES_DIRS = (BASE_DIR / "staticfiles",)

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

LOCALE_PATHS = [
    BASE_DIR / 'locale/',
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# CACHES
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"{env.str('REDIS_URL', 'redis://localhost:6379/0')}",
        "KEY_PREFIX": "tranzit-backend",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

# CELERY CONFIGURATION
CELERY_BROKER_URL = env.str("CELERY_BROKER_URL", "redis://localhost:6379")
CELERY_RESULT_BACKEND = env.str("CELERY_BROKER_URL", "redis://localhost:6379")

CELERY_TIMEZONE = "Asia/Tashkent"

CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60

FIREBASE_APP = initialize_app()
FCM_DJANGO_SETTINGS = {
    "DEFAULT_FIREBASE_APP": None,
    "APP_VERBOSE_NAME": _("Devices"),
    "ONE_DEVICE_PER_USER": True,
    "DELETE_INACTIVE_DEVICES": True,
    "FCM_SERVER_KEY": env.str(
        "FCM_SERVER_KEY",
        "AAAAf-BdT7Q:APA91bF3IkaVvmd3CmCOH8J4ugLCk6MJ52PzY4c3pp5IC1eh8JVnE9a4Ym6_jkChMBWqWndcxhCIxBGuSuMvmp5tMflGfI_2288AJ814V1qdyN-uBzdMXAQm1PbXlDZAzUnBlyHEnixK",
    ),
}


def gettext(s):
    return s


LANGUAGES = (
    ("uz", "Uzbek"),
    ("ru", "Russian"),
    ("en", "English"),
)

MODELTRANSLATION_DEFAULT_LANGUAGE = "ru"
MODELTRANSLATION_LANGUAGES = (
    "uz",
    "ru",
    "en",
)
MODELTRANSLATION_FALLBACK_LANGUAGES = {
    "default": (
        "uz",
        "ru",
        "en",
    ),
    "uz": (
        "ru",
        "en",
    ),
    "en": (
        "uz",
        "ru",
    ),
    "ru": (
        "uz",
        "en",
    ),
}

MODELTRANSLATION_PREPOPULATE_LANGUAGE = "ru"

ESKIZ_EMAIL = env.str("ESKIZ_USER_EMAIL", "u.shakhriyor27@gmail.com")
ESKIZ_PASSWORD = env.str("ESKIZ_USER_PASSWORD", "SLIubboHI2uw0NMqoeObRmsZF4qqCL29FgP9cvLH")

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [env.str("REDIS_URL")],
        },
    },
}

# SWAGGER SETTINGS
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {"api_key": {"type": "apiKey", "in": "header", "name": "Authorization"}},
}

# SIMPLE JWT SETTINGS
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=120),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}

RECAPTCHA_PUBLIC_KEY = '6LfToDgoAAAAACIY8N9T-ErIhc1Z-dkZWUSUj2IQ'
RECAPTCHA_PRIVATE_KEY = '6LfToDgoAAAAALdclfq6rUacx-l-VE0DJP9j8Ht0'

PAYMENT_CREDENTIALS = {
    "payme": {
        "callback_url": "https://checkout.paycom.uz",
        "merchant_id": env.str("PAYME_MERCHANT_ID", ''),
        'test_secret_key': env.str("PAYME_TEST_SECRET_KEY", ''),
        'secret_key': env.str("PAYME_SECRET_KEY", ''),
        'credential_key': 'order_id',
        'subscribe_base_url': env.str("PAYME_SUBSCRIBE_BASE_URL", ""),
        "subscribe_paycom_id": env.str("PAYME_SUBSCRIBE_PAYCOM_ID", "")
    },
    "click": {
        "callback_url": "https://my.click.uz/services/pay",
        "merchant_id": env.str("CLICK_MERCHANT_ID", ""),
        "merchant_service_id": env.str("CLICK_MERCHANT_SERVICE_ID", ""),
        "merchant_user_id": env.str("CLICK_MERCHANT_USER_ID", ""),
        "secret_key": env.str("CLICK_SECRET_KEY", ""),
    },

}

sentry_sdk.init(
    dsn=env.str("SENTRY_DSN", ''),
    integrations=[DjangoIntegration(), FastApiIntegration()],
    before_send=before_send_trigger,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)


OCPP_SERVER_START_URL = env.str("OCPP_SERVER_START_URL", "http://localhost:8080")
OCPP_SERVER_STOP_URL = env.str("OCPP_SERVER_STOP_URL", "http://localhost:8080")


IMPORT_EXPORT_SKIP_ADMIN_ACTION_EXPORT_UI = True
IMPORT_EXPORT_SKIP_ADMIN_CONFIRM = True
EXPORT_FORMATS = [XLSX]


CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "full",
        "height": 400,
        "width": 550,
    },
}

CKEDITOR_UPLOAD_PATH = "uploads/"
