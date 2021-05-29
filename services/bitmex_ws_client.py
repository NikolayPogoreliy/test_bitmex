from bitmex_websocket import BitMEXWebsocket


class BitmexWsClient:

    def __init__(self):
        self.ws_client = BitMEXWebsocket(
            endpoint="https://testnet.bitmex.com/api/v1",
            api_key=None,
            symbol='XBTUSD',
            api_secret=None
        )

    def get_instrument(self):
        return self.ws_client.get_instrument()

    def close(self):
        return self.ws_client.exit()
