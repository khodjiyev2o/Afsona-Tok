from rest_framework.generics import RetrieveAPIView

from apps.chargers.api_endpoints.ChargingTransactionDetail.serializers import ChargingTransactionDetailSerializer
from apps.chargers.models import ChargingTransaction


class ChargingTransactionDetailAPIView(RetrieveAPIView):
    serializer_class = ChargingTransactionDetailSerializer
    queryset = ChargingTransaction.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('connector__charge_point__location')

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        queryset = queryset.filter(
            user_id=self.request.user.id,
            status=ChargingTransaction.Status.FINISHED
        )
        return queryset


__all__ = ['ChargingTransactionDetailAPIView']
