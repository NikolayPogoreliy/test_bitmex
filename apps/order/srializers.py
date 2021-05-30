from rest_framework import serializers

from apps.order.models import Order


class OrderSerializer(serializers.ModelSerializer):
    account_name = serializers.CharField(read_only=True)
    author_account = serializers.PrimaryKeyRelatedField(read_only=True)
    account = serializers.IntegerField(read_only=True)
    status = serializers.CharField(read_only=True)
    order_id = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
