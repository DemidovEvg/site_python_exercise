import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
import redis
from django.conf import settings
from channels.db import database_sync_to_async
import pickle


redis_instance = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0
)


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        """
        Ключ текущего канала формируется под капотом:
        self.channel_name
        Ключ группы формируем сами(либо можно задать для класса):
        self.room_group_name
        Контекст запроса:
        self.scope
        """

        from pprint import pprint
        pprint(self.scope)
        print(f"def connect(self) {self.scope['url_route']}")
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        print(f'channel_name: {self.channel_name}')

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):

        print(f'def disconnect(self, close_code) {close_code}')
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    def clean_room(self, room_group_name):
        redis_instance.delete(room_group_name)

    async def receive(self, text_data):
        print(f'def receive(self, text_data) {text_data}')
        print(f'channel_name: {self.channel_name}')
        text_data_json = json.loads(text_data)

        output_data = {
            'type': 'chat_message',
            'channel_name': self.channel_name,
        }

        # Здесь будет роутер
        event = text_data_json.get('event', None)
        if event and event == 'clean':
            await database_sync_to_async(self.clean_room)(self.room_group_name)
        else:
            message = text_data_json['message']
            output_data['message'] = message
            # Пример работы с бд:
            await database_sync_to_async(self.save_messages)(
                self.room_group_name,
                self.channel_name,
                message
            )

        await self.channel_layer.group_send(
            self.room_group_name,
            output_data
        )

    def save_messages(self, room_group_name, channel_name, message):
        parcel = {
            'channel_name': channel_name,
            'message': message
        }
        parcel = pickle.dumps(parcel)
        redis_instance.lpush(room_group_name, parcel)

    async def chat_message(self, event):
        print(f'111111111111111def chat_message(self, event) {event}')

        # message = event['message']

        parcels = await database_sync_to_async(self.get_messages)(
            self.room_group_name
        )
        print(parcels)

        output_data = {
            'parcels': parcels
        }

        await self.send(text_data=json.dumps(output_data))

    def get_messages(self, room_group_name):
        parcels = redis_instance.lrange(room_group_name, 0, -1)
        parcels = list(map(lambda el: pickle.loads(el), parcels))
        print(parcels)
        return parcels
