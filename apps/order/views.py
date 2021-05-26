from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

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
    permission_classes = (IsAuthenticated, )
    filter_backends = (DjangoFilterBackend, )
    filter_class = OrderFilter

    def retrieve(self, request, pk=None, account_name=None, *args, **kwargs):
        order = self.get_object()
        client = BitmexClient(order.account)
        results = client.order_retrieve(order.order_id)
        return Response(results)

    def list(self, request, *args, **kwargs):
        pass
