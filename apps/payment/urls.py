from django.urls import path

from apps.payment.payment_types.payme.merchant.views import PaymeCallbackView
from apps.payment.payment_types.click_merchant.Prepare.views import ClickPrepareAPIView
from apps.payment.payment_types.click_merchant.Complete.views import ClickCompleteAPIView

from apps.payment.api_endpoints import * # noqa
from apps.payment.payment_types.payme import * # noqa

app_name = 'payment'

urlpatterns = [
    path("TransactionCreate/", TransactionCreateView.as_view(), name="transaction-create"),
    path("TransactionDetail/", TransactionDetailView.as_view(), name="transaction-detail"),
    path("UserCardList/", UserCardListView.as_view(), name="user-card-list"),
    path("CardCreate/", UserCardCreateView.as_view(), name="user-card-create"),
    path("CardVerify/", UserCardVerifyAPIView.as_view(), name="user-card-verify"),
    path("ReceiptPay/", ReceiptPayView.as_view(), name="receipt-pay"),
    path("CardIdentify/", CardIdentifyView.as_view(), name="card-identify"),

    # payment webhooks
    path("payme/", PaymeCallbackView.as_view(), name="payme"),
    path("click/Prepare/", ClickPrepareAPIView.as_view(), name="click-prepare"),
    path("click/Complete/", ClickCompleteAPIView.as_view(), name="click-complete"),
]
