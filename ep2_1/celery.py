import logging
import os

import celery
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ep2_1.settings')

celery_app = Celery('ep2_1')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
# celery_app.autodiscover_tasks()


@celery.signals.after_setup_logger.connect
def on_after_setup_logger(**kwargs):
    logger = logging.getLogger('celery')
    logger.propagate = True
    logger = logging.getLogger('celery.app.trace')
    logger.propagate = True


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(1.0, get_report.s(),)


@celery_app.task
def get_report():
    # logger.debug('Start task')
    raise Exception
    print("AZAZAZ")
    channel_layer = get_channel_layer()
    if not ws_list:
        ws_list.append(BitmexWsClient())
    results = ws_list[0].get_instrument()
    print(id(ws_list[0]))
    # logger.debug(results)
    data = {
        'timestamp': results.get('timestamp'),
        'symbol': results.get('symbol'),
        'price': results.get('lastPrice')
    }
    # logger.debug(data)
    async_to_sync(channel_layer.group_send)(
        "bitmex_feed",
        {
            "type": "bitmex_feed.feed_message",
            "message": json.dumps(data),
        },
    )