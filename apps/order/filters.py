from django_filters import rest_framework as filters

from apps.order.models import Order


class OrderFilter(filters.FilterSet):
    class Meta:
        model = Order
        fields = ('author_account__id', 'side', 'symbol', 'status')
