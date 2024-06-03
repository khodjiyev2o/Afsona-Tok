from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.common.api_endpoints.UserAppealCreate.serializers import UserAppealCreateSerializer
from apps.common.models import UserAppeal


class UserAppealCreateView(generics.CreateAPIView):
    queryset = UserAppeal.objects.all()
    serializer_class = UserAppealCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


__all__ = ['UserAppealCreateView']
