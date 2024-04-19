from django.db import transaction
from rest_framework.views import APIView

from apps.payment.models import MerchantRequestLog, Transaction


class PaymentView(APIView):
    TYPE: str = ""
    PROVIDER: str = ""
    permission_classes = []

    @transaction.non_atomic_requests
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        MerchantRequestLog.objects.create(
            payment_type=Transaction.PaymentType.CLICK,
            method_type=self.TYPE,
            request_headers=self.request.headers,
            request_body=dict(self.request.data),
            response_status_code=response.status_code,
            response_body=response.data,
        )
        return response
