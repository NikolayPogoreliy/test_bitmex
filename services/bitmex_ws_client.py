import json

from asgiref.sync import async_to_sync
from bitmex_websocket import BitMEXWebsocket
from channels.layers import get_channel_layer


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class GwBitMEXWebsocket(BitMEXWebsocket, metaclass=Singleton):

    def __init__(self, endpoint, symbol: str, api_key: str = None, api_secret: str = None,
                 subscriptions: list = None, ):
        self.user_subscription = subscriptions or ['instrument']
        self.channel_layer = get_channel_layer()
        super().__init__(endpoint, symbol, api_key, api_secret)

    def __on_message(self, message):
        '''Handler for parsing WS messages.'''
        message = json.loads(message)
        print(message)
        if message['subscribe'] in self.user_subscription:
            # channel_layer = get_channel_layer()
            results = message.get('data')[0]
            data = {
                'timestamp': results.get('timestamp'), 'symbol': results.get('symbol'),
                'price': results.get('markPrice')}
            print(data)
            async_to_sync(self.channel_layer.group_send)("bitmex_feed", {
                "type": "bitmex_feed.feed_message", "message": json.dumps(data), }, )
        self._BitMEXWebsocket__on_message(message)


class BitmexWsClient:

    def __init__(self):
        self.ws_client = GwBitMEXWebsocket(endpoint="https://testnet.bitmex.com/api/v1", api_key=None, symbol='XBTUSD',
            api_secret=None)

    def get_instrument(self):
        return self.ws_client.get_instrument()

    def close(self):
        return self.ws_client.exit()
