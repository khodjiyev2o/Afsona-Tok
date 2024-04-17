from rest_framework import generics

from apps.common.api_endpoints.MainSettings.serializers import MainSettingsSerializer
from apps.common.models import MainSettings


class MainSettingsView(generics.RetrieveAPIView):
    queryset = MainSettings.objects.all()
    serializer_class = MainSettingsSerializer

    def get_object(self):
        return MainSettings.objects.first()


__all__ = ['MainSettingsView']
