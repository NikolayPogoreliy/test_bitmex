# from ep2_1 import celery_app

# logger = get_task_logger(__name__)

ws_list = []
# @celery_app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(10.0, get_report.s(),)


# @shared_task
# def get_report():
#     # logger.debug('Start task')
#     raise Exception
#     print("AZAZAZ")
#     channel_layer = get_channel_layer()
#     if not ws_list:
#         ws_list.append(BitmexWsClient())
#     results = ws_list[0].get_instrument()
#     print(id(ws_list[0]))
#     # logger.debug(results)
#     data = {
#         'timestamp': results.get('timestamp'),
#         'symbol': results.get('symbol'),
#         'price': results.get('lastPrice')
#     }
#     # logger.debug(data)
#     async_to_sync(channel_layer.group_send)(
#         "bitmex_feed",
#         {
#             "type": "bitmex_feed.feed_message",
#             "message": json.dumps(data),
#         },
#     )
