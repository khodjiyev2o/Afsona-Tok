from rest_framework import generics

from apps.chargers.api_endpoints.ChargingTransactionList.serializers import ChargingTransactionListSerializer
from apps.chargers.models import ChargingTransaction


class ChargingTransactionListAPIView(generics.ListAPIView):
    serializer_class = ChargingTransactionListSerializer
    queryset = ChargingTransaction.objects.all().order_by('-created_at')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related(
            'connector',
            'connector__charge_point__location',
            'user_car',
            'user_car__model',
            'user_car__manufacturer'
        )
        return queryset

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        queryset = queryset.filter(
            user_id=self.request.user.id,
            status=ChargingTransaction.Status.FINISHED
        )
        return queryset


__all__ = ['ChargingTransactionListAPIView']
