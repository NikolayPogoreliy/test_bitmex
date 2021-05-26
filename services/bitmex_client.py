import bitmex

from apps.account.models import Account


class BitmexClient:

    def __init__(self, account: Account):
        self.client = bitmex.bitmex(api_key=account.api_key, api_secret=account.api_secret)

    def place_order(
        self,
        symbol,
        volume,
        side,
        price
    ):
        return self.client.Order.Order_new(symbol=symbol, orderQty=volume, price=price, side=side).result()

    def order_list(self):
        return self.client.Order.Order_getOrders().result()

    def order_retrieve(self, order_id):
        return self.client.Order.Order_getOrders(filter={'orderID': order_id}).result()
