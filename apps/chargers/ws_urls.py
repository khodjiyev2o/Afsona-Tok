from django.urls import path
from apps.chargers.consumers import MobileJsonConsumer


websocket_urlpatterns = [
    path('api/ws/v1/connectors/', MobileJsonConsumer.as_asgi()),
]
