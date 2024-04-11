from django.urls import path
from apps.chargers.consumers import EchoConsumer


websocket_urlpatterns = [
    path('api/ws/v1/connectors/', EchoConsumer.as_asgi()),
    path('api/ws/v1/trancaction/<int:pk>/', EchoConsumer.as_asgi()),
]
