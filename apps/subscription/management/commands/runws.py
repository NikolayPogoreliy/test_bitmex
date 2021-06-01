import asyncio
import json

import websockets
from channels.layers import get_channel_layer


# CHANNEL_LAYERS = settings.CHANNEL_LAYERS



async def message_handler(ws):
    async for message in ws:
        message = json.loads(message)
        if message.get('table') == 'instrument' or message.get('subscribe') == 'instrument':
            channel_layer = get_channel_layer()
            results = message.get('data')[0]
            price = results.get('markPrice') or results.get('fairPrice')
            if price:
                data = {
                    'timestamp': results.get('timestamp'),
                    'symbol': results.get('symbol'),
                    'price': results.get('markPrice')
                }
                await channel_layer.group_send(
                    "bitmex_feed",
                    {
                        "type": "feed_message",
                        "message": json.dumps(data),
                    },
                )


async def consume(url):
    async with websockets.connect(url) as ws:
        await message_handler(ws)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        consume('wss://testnet.bitmex.com/realtime?subscribe=instrument:XBTUSD')
    )
    loop.run_forever()