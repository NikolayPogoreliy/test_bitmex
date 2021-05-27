from rest_framework import serializers

from apps.order.models import Order


class OrderSerializer(serializers.ModelSerializer):
    author_account = serializers.PrimaryKeyRelatedField(read_only=True)
    account = serializers.IntegerField(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
