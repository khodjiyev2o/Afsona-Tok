from django.urls import path

from apps.payment.payment_types.payme.merchant.views import PaymeCallbackView
from apps.payment.api_endpoints import * # noqa

app_name = 'payment'

urlpatterns = [
    path("TransactionCreate/", TransactionCreateView.as_view(), name="transaction-create"),
    path("payme/", PaymeCallbackView.as_view(), name="payme"),
]
