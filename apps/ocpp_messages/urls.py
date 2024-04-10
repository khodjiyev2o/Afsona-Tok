from django.urls import path
from .views import (
    ChargerDisconnectAPIView, BootNotificationAPIView, HeartbeatAPIView,
    MeterValuesAPIView, StatusNotificationAPIView, StartTransactionAPIView,
    StopTransactionAPIView, CommandCallbackAPIView
)

app_name = 'ocpp_messages'

urlpatterns = [
    path("<str:charger_identify>/boot_notification/", BootNotificationAPIView.as_view()),
    path("<str:charger_identify>/heartbeat/", HeartbeatAPIView.as_view()),
    path('<str:charger_identify>/meter_values/', MeterValuesAPIView.as_view()),
    path("<str:charger_identify>/start_transaction/", StartTransactionAPIView.as_view()),
    path("<str:charger_identify>/status_notification/", StatusNotificationAPIView.as_view()),
    path("<str:charger_identify>/stop_transaction/", StopTransactionAPIView.as_view()),
    path("<str:charger_identify>/disconnect/", ChargerDisconnectAPIView.as_view()),
    path("command-callback/<str:id_tag>/", CommandCallbackAPIView.as_view())
]
