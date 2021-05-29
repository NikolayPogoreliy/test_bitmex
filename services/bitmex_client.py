import json

import bitmex

from apps.account.models import Account


class BitmexClient:

    def __init__(self, account: Account):
        self.client = bitmex.bitmex(api_key=account.api_key, api_secret=account.api_secret)
        return self

    def order_place(
            self,
            symbol,
            volume,
            side,
            price
    ):
        return self.client.Order.Order_new(symbol=symbol, orderQty=volume, price=price, side=side).result()[0]

    def order_list(self):
        return self.client.Order.Order_getOrders().result()[0]

    def order_retrieve(self, order_id):
        return self.client.Order.Order_getOrders(filter=json.dumps({'orderID': order_id})).result()[0]

    def order_delete(self, order_id):
        return self.client.Order.Order_cancel(orderID=order_id).result()[0]
