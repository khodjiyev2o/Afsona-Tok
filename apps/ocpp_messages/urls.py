from django.urls import path
from .views import (
    ChargerDisconnectAPIView, BootNotificationApiView, HeartbeatApiView,
    MeterValuesApiView, StatusNotificationApiView, StartTransactionApiView,
    StopTransactionApiView,CommandCallbackAPIView
)

app_name = 'ocpp_messages'

urlpatterns = [
    path("<str:charger_identify>/boot_notification/", BootNotificationApiView.as_view()),
    path("<str:charger_identify>/heartbeat/", HeartbeatApiView.as_view()),
    path('<str:charger_identify>/meter_values/', MeterValuesApiView.as_view()),
    path("<str:charger_identify>/start_transaction/", StartTransactionApiView.as_view()),
    path("<str:charger_identify>/status_notification", StatusNotificationApiView.as_view()),
    path("<str:charger_identify>/stop_transaction", StopTransactionApiView.as_view()),
    path("<str:charger_identify>/disconnect/", ChargerDisconnectAPIView.as_view()),
    path("command-callback/<str:id_tag>/", CommandCallbackAPIView.as_view())
]