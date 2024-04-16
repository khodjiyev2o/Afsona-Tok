from django.urls import path

from apps.payment.payment_types.payme_merchant.views import PaymeCallbackView

app_name = 'payment'

urlpatterns = [
    path("payme/", PaymeCallbackView.as_view(), name="payme"),
]