from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.common.api_endpoints.UserCarEdit.serializers import UserCarEditSerializer
from apps.common.models import UserCar


class UserCarEditView(generics.UpdateAPIView):
    """Edit user car"""
    serializer_class = UserCarEditSerializer
    queryset = UserCar.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


__all__ = ['UserCarEditView']
