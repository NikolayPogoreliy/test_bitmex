import json
import os

from asgiref.sync import async_to_sync
from celery import Celery
from celery.utils.log import get_task_logger
from channels.layers import get_channel_layer

from services.bitmex_ws_client import BitmexWsClient

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ep2_1.settings')

celery_app = Celery('ep2_1')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
# celery_app.autodiscover_tasks()
ws_list = []

logger = get_task_logger(__name__)


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(5.0, get_report.s(), )


@celery_app.task
def get_report():
    # logger.debug('Start task')
    channel_layer = get_channel_layer()
    if not ws_list:
        ws_list.append(BitmexWsClient())
    results = ws_list[0].get_instrument()
    data = {
        'timestamp': results.get('timestamp'),
        'symbol': results.get('symbol'),
        'price': results.get('lastPrice')
    }
    logger.debug(data)
    async_to_sync(channel_layer.group_send)("bitmex_feed", {
        "type": "bitmex_feed.feed_message", "message": json.dumps(data), }, )
