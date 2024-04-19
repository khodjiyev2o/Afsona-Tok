from django.urls import path

from apps.payment.payment_types.payme.merchant.views import PaymeCallbackView
from apps.payment.payment_types.click_merchant.Prepare.views import ClickPrepareAPIView
from apps.payment.payment_types.click_merchant.Complete.views import ClickCompleteAPIView

from apps.payment.api_endpoints import * # noqa

app_name = 'payment'

urlpatterns = [
    path("TransactionCreate/", TransactionCreateView.as_view(), name="transaction-create"),
    path("payme/", PaymeCallbackView.as_view(), name="payme"),
    path("click/Prepare/", ClickPrepareAPIView.as_view(), name="click-prepare"),
    path("click/Complete/", ClickCompleteAPIView.as_view(), name="click-complete"),
]
