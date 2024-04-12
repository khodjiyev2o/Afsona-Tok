from django.urls import path
from apps.chargers.consumers import MobileJsonConsumer


websocket_urlpatterns = [
    path('api/ws/v1/mobile/', MobileJsonConsumer.as_asgi()),
]
