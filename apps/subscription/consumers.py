import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.shortcuts import get_object_or_404

from apps.account.models import Account
from apps.subscription.models import Subscriber


# TODO: add bitmex-ws


class SubscriptionConsumer(AsyncJsonWebsocketConsumer):
    room_group_name = 'bitmex_feed'

    async def connect(self):
        await self.accept()

    async def websocket_connect(self, message):
        await super().websocket_connect(message)

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive_json(self, content, **kwargs):
        message = content['message']
        account = get_object_or_404(Account, name=message.get('account'))
        self.scope['session']['account'] = account.name
        if message.get('action') == 'subscribe':
            Subscriber.objects.get_or_create(account=account)  # TODO: do we need it?
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
        elif message.get('action') == 'unsubscribe':
            Subscriber.objects.filter(account=account).delete()  # TODO: do we need it?
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
            await self.close()
        # Send message to room group
        # await self.channel_layer.group_send(
        #     self.room_group_name,
        #     {
        #         'type': 'feed_message',
        #         'message': message
        #     }
        # )

    # Receive message from room group
    async def feed_message(self, event):
        message = json.loads(event['message'])

        # Send message to WebSocket
        message.update({'account': self.scope['session']['account']})
        print(message)
        await self.send_json(content=message)
