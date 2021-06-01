from django.apps import AppConfig

from services.bitmex_ws_client import GwBitMEXWebsocket


class SubscriptionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.subscription'

    def ready(self):
        GwBitMEXWebsocket(endpoint="https://testnet.bitmex.com/api/v1", api_key=None, symbol='XBTUSD', api_secret=None)

