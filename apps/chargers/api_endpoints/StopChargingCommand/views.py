from rest_framework.generics import CreateAPIView

from apps.chargers.models import ChargeCommand
from .serializers import StopChargingCommandSerializer


class StopChargingCommandView(CreateAPIView):
    queryset = ChargeCommand.objects.all()
    serializer_class = StopChargingCommandSerializer
