import os
from pathlib import Path

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from apps.chargers.ws_auth import WebsocketJWTAuthMiddleware
from apps.chargers.ws_urls import websocket_urlpatterns
import environ


def get_application():
    environ.Env().read_env(env_file=os.path.join(Path(__file__).resolve().parent.parent.joinpath('.env')))
    return ProtocolTypeRouter({
        "http": get_asgi_application(),
        "websocket":
            AuthMiddlewareStack(
                WebsocketJWTAuthMiddleware(
                    URLRouter(
                        websocket_urlpatterns
                    ),
                )
            )
    }
    )


application = get_application()
