from django.urls import path
from .views import (
    default_index, BootNotificationApiView, HeartbeatApiView,
    MeterValuesApiView, StatusNotificationApiView,
)

app_name = 'ocpp_messages'

urlpatterns = [
    path("<str:charger_identify>/boot_notification/", BootNotificationApiView.as_view()),
    path("<str:charger_identify>/heartbeat/", HeartbeatApiView.as_view()),
    path('<str:charger_identify>/meter_values/', MeterValuesApiView),
    path("<str:charger_identify>/start_transaction/", default_index),
    path("<str:charger_identify>/status_notification", StatusNotificationApiView),
    path("<str:charger_identify>/stop_transaction", default_index),
    path("<str:charger_identify>/disonnect/", default_index)
]