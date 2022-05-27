from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws://b-mocks.dev.app.getbaraka.com:9989/$', consumers.StockDataConsumer.as_asgi()),
]