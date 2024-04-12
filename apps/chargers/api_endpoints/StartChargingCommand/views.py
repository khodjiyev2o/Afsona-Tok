from rest_framework.generics import CreateAPIView

from apps.chargers.models import ChargeCommand
from .serializers import StartChargingCommandSerializer


class StartChargingCommandView(CreateAPIView):
    queryset = ChargeCommand.objects.all()
    serializer_class = StartChargingCommandSerializer
