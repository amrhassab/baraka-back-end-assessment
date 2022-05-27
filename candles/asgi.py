import os

import django
from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import stockdata.routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'candles.settings')
django.setup()

application = ProtocolTypeRouter({
    "http": AsgiHandler(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            stockdata.routing.websocket_urlpatterns
        )
    ),
})
