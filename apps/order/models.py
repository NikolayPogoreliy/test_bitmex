from django.db import models

from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class OrdersideChoices(TextChoices):
    BUY = 'Buy', _('Buy')
    SELL = 'Sell', _('Sell')


class Order(models.Model):
    order_id = models.CharField(max_length=36, unique=True)
    symbol = models.CharField(max_length=6)
    volume = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    side = models.CharField(max_length=4, choices=OrdersideChoices.choices, default=OrdersideChoices.BUY)
    price = models.IntegerField(null=True)
    author_account = models.ForeignKey('account.Account', on_delete=models.CASCADE, null=True)
    account = models.PositiveIntegerField(null=True)
    status = models.CharField(max_length=15, blank=True, null=True)
