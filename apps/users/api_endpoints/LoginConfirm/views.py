from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView

from apps.users.api_endpoints.LoginConfirm.serializers import LoginConfirmSerializer

User = get_user_model()


class LoginConfirmAPIView(CreateAPIView):
    serializer_class = LoginConfirmSerializer
    queryset = User.objects.all()
