from aiogram import Bot
from aiogram.types import ChatIdUnion

from src.decorators.safe import safe


class SafeBot(Bot):
    @safe
    async def send_message(self, chat_id: int, text: str, **kwargs):
        return await super().send_message(chat_id, text=text, **kwargs)

    @safe
    async def send_video_note(self, chat_id: int, video_note, **kwargs):
        return await super().send_video_note(chat_id, video_note=video_note, **kwargs)

    @safe
    async def send_video(self, chat_id: int, video, **kwargs):
        return await super().send_video(chat_id, video=video, **kwargs)

    @safe
    async def send_photo(self, chat_id: int, photo, **kwargs):
        return await super().send_photo(chat_id, photo=photo, **kwargs)

    @safe
    async def send_document(self, chat_id: int, document, **kwargs):
        return await super().send_document(chat_id, document=document, **kwargs)

    @safe
    async def send_audio(self, chat_id: int, audio, **kwargs):
        return await super().send_audio(chat_id, audio=audio, **kwargs)

    @safe
    async def send_animation(self, chat_id: int, animation, **kwargs):
        return await super().send_animation(chat_id, animation=animation, **kwargs)

    @safe
    async def delete_message(
        self,
        chat_id: ChatIdUnion,
        message_id: int,
        request_timeout: int | None = None,
    ) -> bool:
        return await super().delete_message(chat_id, message_id=message_id, request_timeout=request_timeout)