from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.api_endpoints.LoginConfirm.serializers import LoginConfirmSerializer
from apps.users.models import User


class LoginConfirmView(APIView):
    serializer_class = LoginConfirmSerializer

    @swagger_auto_schema(request_body=LoginConfirmSerializer)
    def post(self, request, *args, **kwargs):
        serializer = LoginConfirmSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            phone = serializer.validated_data.get("phone")
            user, _c = User.objects.get_or_create(phone=phone)
            is_new = True if not user.date_of_birth else False

            return Response({"is_new": is_new,  "access_token": user.tokens['access'],
                             "refresh_token": user.tokens['refresh']},  status=200)


__all__ = ['LoginConfirmView']
