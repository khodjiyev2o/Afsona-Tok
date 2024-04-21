from rest_framework.generics import ListAPIView

from apps.chargers.api_endpoints.InProgressChargingTransactionList.serializers import \
    InProgressChargingTransactionListSerializer
from apps.chargers.models import ChargingTransaction


class InProgressChargingTransactionListAPIView(ListAPIView):
    serializer_class = InProgressChargingTransactionListSerializer
    queryset = ChargingTransaction.objects.all()
    pagination_class = None

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related(
            'user_car',
            'user_car__model',
            'user_car__manufacturer',
            'connector',
            'connector__standard'
        )

        return queryset

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        queryset = queryset.filter(
            user_id=self.request.user.id,
            status=ChargingTransaction.Status.IN_PROGRESS
        )
        return queryset


__all__ = ['InProgressChargingTransactionListAPIView']
