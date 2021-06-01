import os

from celery import Celery
from celery.utils.log import get_task_logger
from django.conf import settings

from services.bitmex_ws_client import GwBitMEXWebsocket

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ep2_1.settings')

celery_app = Celery('ep2_1')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()


logger = get_task_logger(__name__)


@celery_app.task
def get_report():
    """
    Get recent info about instruments and feed it to the ws-group for subscribers
    """
    if not settings.WS_LIST:
        settings.WS_LIST.append(GwBitMEXWebsocket(
            endpoint="https://testnet.bitmex.com/api/v1",
            api_key=None,
            symbol='XBTUSD',
            api_secret=None))
