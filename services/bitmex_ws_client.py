import json

from asgiref.sync import async_to_sync
from bitmex_websocket import BitMEXWebsocket
from channels.layers import get_channel_layer


class GwBitMEXWebsocket(BitMEXWebsocket):

    def __init__(self, endpoint, symbol: str, api_key: str = None, api_secret: str = None, subscriptions: list = None):
        self.user_subscription = subscriptions
        super().__init__(endpoint, symbol, api_key, api_secret)

    def __on_message(self, message):
        '''Handler for parsing WS messages.'''
        message = json.loads(message)
        if message['subscribe'] in self.user_subscription:
            channel_layer = get_channel_layer()
            results=message.get('data')
            data = {
                'timestamp': results.get('timestamp'),
                'symbol': results.get('symbol'),
                'price': results.get('lastPrice')
            }
            # logger.debug(data)
            async_to_sync(channel_layer.group_send)("bitmex_feed", {
                "type": "bitmex_feed.feed_message", "message": json.dumps(data),
            }, )
        self._BitMEXWebsocket__on_message(message)


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
