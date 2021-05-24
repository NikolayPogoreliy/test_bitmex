from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.order.models import Order
from apps.order.srializers import OrderSerializer


class OrderView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated, )
