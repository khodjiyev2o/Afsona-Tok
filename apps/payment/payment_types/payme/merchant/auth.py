import base64
import binascii

from django.conf import settings
from rest_framework import HTTP_HEADER_ENCODING
from rest_framework.authentication import BasicAuthentication, get_authorization_header


class PaymeBasicAuthentication(BasicAuthentication):
    def authenticate(self, request):
        USERNAME = settings.PAYMENT_CREDENTIALS['payme']['merchant_id']
        TEST_PASSWORD = settings.PAYMENT_CREDENTIALS['payme']['test_secret_key']
        PASSWORD = settings.PAYMENT_CREDENTIALS['payme']['secret_key']

        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != b"basic":
            return None, None

        if len(auth) != 2:
            return None, None

        try:
            username, *_, password = base64.b64decode(auth[1]).decode(HTTP_HEADER_ENCODING).partition(":")
        except (TypeError, UnicodeDecodeError, binascii.Error):
            return None, None

        if username in ["Paycom", USERNAME] and password in [PASSWORD, TEST_PASSWORD]:
            return True, None

        return None, None
