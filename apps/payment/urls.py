from django.urls import path

from apps.payment.payment_types.payme.merchant.views import PaymeCallbackView
from apps.payment.payment_types.click_merchant.Prepare.views import ClickPrepareAPIView
from apps.payment.payment_types.click_merchant.Complete.views import ClickCompleteAPIView

from apps.payment.api_endpoints import * # noqa
from apps.payment.payment_types.payme import * # noqa

app_name = 'payment'

urlpatterns = [
    path("TransactionCreate/", TransactionCreateView.as_view(), name="transaction-create"),
    path("UserCardList/", UserCardListView.as_view(), name="user-card-list"),
    path("CardCreate/", UserCardCreateView.as_view(), name="user-card-create"),
    path("CardVerify/", UserCardVerifyAPIView.as_view(), name="user-card-verify"),
    # path("DeleteCard/<str:card_id>/", api_endpoints.UserCardDeleteAPIView.as_view(), name="user_card_delete"),
    # path("Transactions/", api_endpoints.TransactionListAPIView.as_view(), name="transactions"),
    path("CardIdentify/", CardIdentifyView.as_view(), name="card-identify"),


    path("payme/", PaymeCallbackView.as_view(), name="payme"),
    path("click/Prepare/", ClickPrepareAPIView.as_view(), name="click-prepare"),
    path("click/Complete/", ClickCompleteAPIView.as_view(), name="click-complete"),
]
