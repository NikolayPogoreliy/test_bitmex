from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import mixins, exceptions
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_api_key.permissions import HasAPIKey

from apps.account.models import Account
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
    debug_permission_classes = (AllowAny,)
    permission_classes = (HasAPIKey,)

    def get_permissions(self):
        if settings.get('DEBUG'):
            permission_classes = self.debug_permission_classes
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]

    def _update_object(self, result, account):
        datas = {
            'order_id': result.get('orderID'), 'author_account': account, 'side': result.get('side'),
            'price': result.get('price'), 'volume': result.get('orderQty'), 'timestamp': result.get('timestamp'),
            'status': result.get('ordStatus'), 'account': result.get('account'), 'symbol': result.get('symbol')}

        order_obj, _ = Order.objects.update_or_create(defaults=datas, order_id=result.get('orderID'))
        result.update({'id': order_obj.id})
        return result

    def retrieve(self, request, account_name: str = None, pk=None, *args, **kwargs):
        """
        Retrieve info about single order (specified by DB-id) for certain account
        """
        account = get_object_or_404(Account, name=account_name)
        order = self.get_object()
        if order.author_account.id != account.id:
            raise exceptions.PermissionDenied('Ypu can not get this order')
        client = BitmexClient(account)
        results = client.order_retrieve(order.order_id)
        return Response(results)

    def list(self, request, account_name: str = None, *args, **kwargs):
        """
        Get list of all orders for certain account
        """
        account = get_object_or_404(Account, name=account_name)
        client = BitmexClient(account)
        results = client.order_list()
        resp = []
        for result in results:
            res = self._update_object(result, account)
            resp.append(res)
        return Response(resp)

    def create(self, request, account_name: str = None, *args, **kwargs):
        """
        Place a new order
        """
        data = request.data
        account = get_object_or_404(Account, name=account_name)

        client = BitmexClient(account)
        result = client.order_place(**data)
        result = self._update_object(result, account)
        return Response(result)

    def destroy(self, request, account_name: str = None, *args, **kwargs):
        """
        Delete (cancel) the order
        """
        account = get_object_or_404(Account, name=account_name)
        order = self.get_object()
        if order.author_account_id != account.id:
            raise exceptions.PermissionDenied('You can not delete this order')
        client = BitmexClient(account)
        result = client.order_delete(order.order_id)[0]
        result = self._update_object(result, account)
        return Response(result)
