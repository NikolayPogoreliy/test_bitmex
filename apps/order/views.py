from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.account.models import Account
from apps.order.filters import OrderFilter
from apps.order.models import Order
from apps.order.srializers import OrderSerializer
from services.bitmex_client import BitmexClient


class OrderView(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # permission_classes = (IsAuthenticated, )
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filter_class = OrderFilter

    def retrieve(self, request, pk=None, account_name=None, *args, **kwargs):
        order = self.get_object()
        client = BitmexClient(order.account)
        results = client.order_retrieve(order.order_id)
        return Response(results)

    def list(self, request, *args, **kwargs):
        account_name = request.query_params.get('account__name')
        account = get_object_or_404(Account, name=account_name)
        client = BitmexClient(account)
        results = client.order_list()
        resp = []
        for result in results:
            datas = {
                'order_id': result.get('orderID'),
                'author_account': account,
                'side': result.get('side'),
                'price': result.get('price'),
                'volume': result.get('orderQty'),
                'timestamp': result.get('timestamp'),
                'status': result.get('ordStatus'),
                'account': result.get('account'),
                'symbol': result.get('symbol')
            }
            order_obj, _ = Order.objects.update_or_create(defaults=datas, order_id=result.get('orderID'))
            result.update({'id': order_obj.id})
            resp.append(result)
        return Response(resp)

    def create(self, request, *args, **kwargs):
        data = request.data
        print(data)
        # data['orderQty'] = data.pop('volume')
        account = get_object_or_404(Account, id=data.pop('account', None))

        client = BitmexClient(account)
        result = client.order_place(**data)
        datas = {
            'order_id': result.get('orderID'),
            'author_account': account,
            'side': result.get('side'),
            'price': result.get('price'),
            'volume': result.get('orderQty'),
            'timestamp': result.get('timestamp'),
            'status': result.get('ordStatus'),
            'account': result.get('account'),
            'symbol': result.get('symbol')
        }

        order_obj, _ = Order.objects.update_or_create(defaults=datas, order_id=result.get('orderID'))
        result.update({'id': order_obj.id})
        return Response(result)
