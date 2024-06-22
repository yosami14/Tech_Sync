from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'techsync.settings')

django_asgi_app = get_asgi_application()

from a_rtchat import routing as a_rtchat_routing
from group import routing as group_routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                a_rtchat_routing.websocket_urlpatterns + group_routing.websocket_urlpatterns
            )
        )
    ),
})