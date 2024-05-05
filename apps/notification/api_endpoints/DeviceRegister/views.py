from fcm_django.models import FCMDevice
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated


class DeviceRegisterView(CreateAPIView):
    queryset = FCMDevice.objects.all()
    serializer_class = DeviceRegisterSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(name=self.request.user.first_name, user=self.request.user)
