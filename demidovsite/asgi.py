import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter
from django.core.asgi import get_asgi_application
from chat.routing import websocket_urlpatterns
import sys

sys.path += os.getcwd() + '\\demidovsite'

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'demidovsite.settings')


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    )
})
