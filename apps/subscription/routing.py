from django.urls import re_path

from apps.subscription import consumers

websocket_urlpatterns = [
    re_path(r'ws/bitmex_feed/$', consumers.SubscriptionConsumer.as_asgi()),
]
