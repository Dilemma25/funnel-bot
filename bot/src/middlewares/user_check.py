from aiogram import BaseMiddleware
from aiogram.types import Message
from src.views.get_or_create_user import get_or_create_user


class UserCheckMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data) -> None:
        if isinstance(event, Message):
            await get_or_create_user(event.from_user.id)
        return await handler(event, data)