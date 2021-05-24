from django.db import models

# Create your models here.
from pgcrypto import fields


class Account(models.Model):
    name = models.CharField(max_length=255, unique=True)
    api_key = models.CharField(max_length=250)
    api_secret = fields.CharPGPSymmetricKeyField(max_length=255)