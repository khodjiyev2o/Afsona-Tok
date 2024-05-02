from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.users.models import User
from apps.users.api_endpoints.UpdateProfile.serializers import ProfileUpdateSerializer


class ProfileUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


__all__ = ["ProfileUpdateView"]
