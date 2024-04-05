from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView

from apps.users.api_endpoints.Login.serializers import LoginSerializer

User = get_user_model()


class LoginAPIView(CreateAPIView):
    serializer_class = LoginSerializer
    queryset = User.objects.all()
