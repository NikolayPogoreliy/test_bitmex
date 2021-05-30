from asgiref.sync import sync_to_async
from django.shortcuts import get_object_or_404


@sync_to_async
def async_get_object_or_404(model, **kwargs):
    return get_object_or_404(model, **kwargs)
