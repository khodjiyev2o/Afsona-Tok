from django.core.cache import cache
from django.utils.crypto import get_random_string
from django.utils.translation import get_supported_language_variant
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.common.utils import send_activation_code_via_sms
from apps.users.api_endpoints.Login.serializers import LoginSmsSerializer
from utils.cache import CacheTypes


class LoginSendSMSView(GenericAPIView):
    serializer_class = LoginSmsSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data.get("phone")
        session = get_random_string(length=16)

        # check if SMS was sent to this phone within 2 minutes for login or registration
        cache_keys = cache.keys(f"{CacheTypes.registration_sms_verification}{str(phone)}*")
        if cache_keys:
            raise ValidationError(detail={"phone": "SMS is already sent!"}, code="timeout")

        # Extract language from Accept-Language header
        accept_language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        language = get_supported_language_variant(accept_language)

        # send 6 digits code to phone
        send_activation_code_via_sms(cache_type=CacheTypes.registration_sms_verification, phone=str(phone),
                                     session=session, language=language)
        return Response({"session": session})


__all__ = ["LoginSendSMSView"]
