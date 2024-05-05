from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from apps.users.api_endpoints.ProfileDetail.serializers import UserProfileSerializer


class ProfileDetailView(RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.prefetch_related("user_notifications")


__all__ = ["ProfileDetailView"]
