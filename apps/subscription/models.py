# Create your models here.
from django.db import models


class Subscriber(models.Model):
    account = models.ForeignKey('account.Account', on_delete=models.CASCADE)
