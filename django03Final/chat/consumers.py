import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

        # Send last 3 messages
        last_messages = await self.get_last_messages(self.room_name)
        for msg in last_messages:
            await self.send(
                text_data=json.dumps(
                    {"message": msg["content"], "username": msg["username"]}
                )
            )

        # Send join message
        user = self.scope["user"]
        if user.is_authenticated:
            username = user.username
            await self.add_user_to_room(self.room_name, user)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": f"{username} has joined the chat",
                    "username": None,  # System message
                },
            )

            await self.send_user_list()

    async def disconnect(self, close_code):
        user = self.scope["user"]
        if user.is_authenticated:
            await self.remove_user_from_room(self.room_name, user)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": f"{user.username} has left the chat",
                    "username": None,  # System message
                },
            )

            await self.send_user_list()

        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user = self.scope["user"]
        username = user.username if user.is_authenticated else "Anonymous"

        if user.is_authenticated:
            await self.save_message(self.room_name, user, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat_message", "message": message, "username": username},
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        username = event.get("username")

        # Send message to WebSocket
        await self.send(
            text_data=json.dumps(
                {"type": "chat_message", "message": message, "username": username}
            )
        )

    async def user_list(self, event):
        users = event["users"]
        await self.send(text_data=json.dumps({"type": "user_list", "users": users}))

    async def send_user_list(self):
        users = await self.get_users_in_room(self.room_name)
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "user_list", "users": users}
        )

    @database_sync_to_async
    def get_last_messages(self, room_name):
        room = Room.objects.get(name=room_name)
        messages = room.messages.order_by("-timestamp")[:3]
        return [
            {"content": msg.content, "username": msg.user.username}
            for msg in reversed(messages)
        ]

    @database_sync_to_async
    def save_message(self, room_name, user, content):
        room = Room.objects.get(name=room_name)
        Message.objects.create(room=room, user=user, content=content)

    @database_sync_to_async
    def add_user_to_room(self, room_name, user):
        room = Room.objects.get(name=room_name)
        room.online_users.add(user)

    @database_sync_to_async
    def remove_user_from_room(self, room_name, user):
        room = Room.objects.get(name=room_name)
        room.online_users.remove(user)

    @database_sync_to_async
    def get_users_in_room(self, room_name):
        room = Room.objects.get(name=room_name)
        return [user.username for user in room.online_users.all()]


