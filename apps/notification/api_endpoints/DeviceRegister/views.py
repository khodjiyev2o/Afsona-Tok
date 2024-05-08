from fcm_django.models import FCMDevice
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.notification.api_endpoints.DeviceRegister.serializers import DeviceRegisterSerializer


class DeviceRegisterView(CreateAPIView):
    queryset = FCMDevice.objects.all()
    serializer_class = DeviceRegisterSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(name=self.request.user.full_name, user=self.request.user)
