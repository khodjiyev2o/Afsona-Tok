from django.urls import path
from apps.chargers.consumers import EchoConsumer


websocket_urlpatterns = [
    path('api/v1/ws/connectors/', EchoConsumer.as_asgi()),
    path('api/v1/ws/trancaction/<int:pk>/', EchoConsumer.as_asgi()),
]
