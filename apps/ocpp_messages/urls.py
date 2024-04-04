from django.urls import path
from .views import default_index

app_name = 'ocpp_messages'

urlpatterns = [
    path("boot_notification/", default_index),
    path("heartbeat/", default_index),
    path('meter_values/', default_index),
    path("start_transaction/", default_index),
    path("status_notification", default_index),
    path("stop_transaction", default_index)
]