# the main routing configuration

from django.urls import re_path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.http import AsgiHandler
import main.routing

application = ProtocolTypeRouter(
    {
        # 'http': URLRouter(main.routing.http_urlpatterns + [re_path(r"", AsgiHandler)]),
        'websocket': AuthMiddlewareStack(URLRouter(main.routing.websocket_urlpatterns)),
    }
)

