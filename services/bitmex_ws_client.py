from bitmex_websocket import BitMEXWebsocket

from apps.account.models import Account


class BitmexWsClient:

    def __init__(self, account: Account):
        self.ws_client = BitMEXWebsocket(
            endpoint="https://testnet.bitmex.com/api/v1",
            symbol="XBTUSD",
            api_key=account.api_key,
            api_secret=account.api_secret
        )

    def get_instrument(self):
        return self.ws_client.get_instrument()
