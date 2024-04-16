from django.urls import path

from apps.payment.providers.payme_merchant.views import PaymeCallbackView

app_name = 'payment'

urlpatterns = [
    path("payme/", PaymeCallbackView.as_view(), name="payme"),
]