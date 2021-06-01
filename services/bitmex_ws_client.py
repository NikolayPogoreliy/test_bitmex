import json
import logging
import threading
import traceback
import urllib
from time import sleep

import websocket
from asgiref.sync import async_to_sync
from bitmex_websocket import BitMEXWebsocket, find_by_keys, order_leaves_quantity
from channels.layers import get_channel_layer
from util.api_key import generate_nonce, generate_signature

logger = logging.getLogger(__name__)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class GwBitMEXWebsocket(BitMEXWebsocket, metaclass=Singleton):

    MAX_TABLE_LEN = 200

    def __init__(self, endpoint, symbol: str = 'XBTUSD', api_key: str = None, api_secret: str = None,
                 subscriptions: list = None, ):
        self.user_subscription = subscriptions or ['instrument']
        self.channel_layer = get_channel_layer()
        '''Connect to the websocket and initialize data stores.'''
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initializing WebSocket.")

        self.endpoint = endpoint
        self.symbols = symbol.split(',')
        self.symbol = self.symbols[0]

        if api_key is not None and api_secret is None:
            raise ValueError('api_secret is required if api_key is provided')
        if api_key is None and api_secret is not None:
            raise ValueError('api_key is required if api_secret is provided')

        self.api_key = api_key
        self.api_secret = api_secret

        self.data = {}
        self.keys = {}
        self.exited = False

        # We can subscribe right in the connection querystring, so let's build that.
        # Subscribe to all pertinent endpoints
        wsURL = self.__get_url()
        self.logger.info("Connecting to %s" % wsURL)
        self.__connect(wsURL, symbol)
        self.logger.info('Connected to WS.')

        # Connected. Wait for partials
        self.__wait_for_symbol(symbol)
        if api_key:
            self.__wait_for_account()
        self.logger.info('Got all market data. Starting.')

    def __connect(self, wsURL, symbol):
        '''Connect to the websocket in a thread.'''
        self.logger.debug("Starting thread")

        self.ws = websocket.WebSocketApp(
            wsURL,
            on_message=self.__on_message,
            on_close=self.__on_close,
            on_open=self.__on_open,
            on_error=self.__on_error,
            header=self.__get_auth()
        )
        self.wst = threading.Thread(target=lambda: self.ws.run_forever())
        self.wst.daemon = True
        self.wst.start()
        self.logger.debug("Started thread")

        # Wait for connect before continuing
        conn_timeout = 5
        while not self.ws.sock or not self.ws.sock.connected and conn_timeout:
            sleep(1)
            conn_timeout -= 1
        if not conn_timeout:
            self.logger.error("Couldn't connect to WS! Exiting.")
            self.exit()
            raise websocket.WebSocketTimeoutException('Couldn\'t connect to WS! Exiting.')

    def __get_auth(self):
        '''Return auth headers. Will use API Keys if present in settings.'''
        if self.api_key:
            self.logger.info("Authenticating with API Key.")
            # To auth to the WS using an API key, we generate a signature of a nonce and
            # the WS API endpoint.
            expires = generate_nonce()
            return ["api-expires: " + str(expires),
                    "api-signature: " + generate_signature(self.api_secret, 'GET', '/realtime', expires, ''),
                    "api-key:" + self.api_key]
        else:
            self.logger.info("Not authenticating.")
            return []

    def __get_url(self):
        '''
        Generate a connection URL. We can define subscriptions right in the querystring.
        Most subscription topics are scoped by the symbol we're listening to.
        '''

        # You can sub to orderBookL2 for all levels, or orderBook10 for top 10 levels & save bandwidth
        symbolSubs = ["execution", "instrument", "order", "orderBookL2", "position", "quote", "trade"]
        genericSubs = ["margin"]

        subscriptions = [sub + ':' + self.symbol for sub in symbolSubs]
        subscriptions += genericSubs

        urlParts = list(urllib.parse.urlparse(self.endpoint))
        urlParts[0] = urlParts[0].replace('http', 'ws')
        urlParts[2] = "/realtime?subscribe={}".format(','.join(subscriptions))
        return urllib.parse.urlunparse(urlParts)

    def __wait_for_account(self):
        '''On subscribe, this data will come down. Wait for it.'''
        # Wait for the keys to show up from the ws
        while not {'margin', 'position', 'order', 'orderBookL2'} <= set(self.data):
            sleep(0.1)

    def __wait_for_symbol(self, symbol):
        '''On subscribe, this data will come down. Wait for it.'''
        while not {'instrument', 'trade', 'quote'} <= set(self.data):
            sleep(0.1)

    def __send_command(self, command, args=None):
        '''Send a raw command.'''
        if args is None:
            args = []
        self.ws.send(json.dumps({"op": command, "args": args}))

    def __on_message(self, message):
        '''Handler for parsing WS messages.'''
        message = json.loads(message)
        self.logger.debug(message)
        if message.get('table') in self.user_subscription or message.get('subscribe') in self.user_subscription:
            self.logger.debug(message)
            results = message.get('data')[0]
            price = results.get('markPrice') or results.get('fairPrice')
            if price:
                data = {
                    'timestamp': results.get('timestamp'),
                    'symbol': results.get('symbol'),
                    'price': results.get('markPrice')
                }
                self.logger.debug(data)
                async_to_sync(self.channel_layer.group_send)("bitmex_feed", {
                    "type": "feed_message", "message": json.dumps(data), }, )

        table = message.get("table")
        action = message.get("action")
        try:
            if table in self.user_subscription:
                if 'subscribe' in message:
                    self.logger.debug("Subscribed to %s." % message['subscribe'])
                elif action:

                    if table not in self.data:
                        self.data[table] = []

                    # There are four possible actions from the WS:
                    # 'partial' - full table image
                    # 'insert'  - new row
                    # 'update'  - update row
                    # 'delete'  - delete row
                    if action == 'partial':
                        self.logger.debug("%s: partial" % table)
                        self.data[table] = message['data']
                        # Keys are communicated on partials to let you know how to uniquely identify
                        # an item. We use it for updates.
                        self.keys[table] = message['keys']
                    elif action == 'insert':
                        self.logger.debug('%s: inserting %s' % (table, message['data']))
                        self.data[table] += message['data']

                        # Limit the max length of the table to avoid excessive memory usage.
                        # Don't trim orders because we'll lose valuable state if we do.
                        if table not in ['order', 'orderBookL2'] and len(
                                self.data[table]) > BitMEXWebsocket.MAX_TABLE_LEN:
                            self.data[table] = self.data[table][BitMEXWebsocket.MAX_TABLE_LEN // 2:]

                    elif action == 'update':
                        self.logger.debug('%s: updating %s' % (table, message['data']))
                        # Locate the item in the collection and update it.
                        for updateData in message['data']:
                            item = find_by_keys(self.keys[table], self.data[table], updateData)
                            if not item:
                                return  # No item found to update. Could happen before push
                            item.update(updateData)
                            # Remove cancelled / filled orders
                            if table == 'order' and not order_leaves_quantity(item):
                                self.data[table].remove(item)
                    elif action == 'delete':
                        self.logger.debug('%s: deleting %s' % (table, message['data']))
                        # Locate the item in the collection and remove it.
                        for deleteData in message['data']:
                            item = find_by_keys(self.keys[table], self.data[table], deleteData)
                            self.data[table].remove(item)
                    else:
                        raise Exception("Unknown action: %s" % action)
        except:
            self.logger.error(traceback.format_exc())

    def __on_error(self, error):
        '''Called on fatal websocket errors. We exit on these.'''
        if not self.exited:
            self.logger.error("Error : %s" % error)
            raise websocket.WebSocketException(error)

    def __on_open(self):
        '''Called when the WS opens.'''
        self.logger.debug("Websocket Opened.")
        for symbol in self.symbols:
            self.__send_command('subscribe', args=[f'instrument:{symbol}'])

    def __on_close(self):
        '''Called on websocket close.'''
        self.logger.info('Websocket Closed')
