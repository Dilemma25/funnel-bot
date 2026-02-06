from aiogram import Bot
from src.decorators.safe_send import safe_send


class SafeBot(Bot):
    @safe_send
    async def send_message(self, chat_id: int, text: str, **kwargs):
        return await super().send_message(chat_id, text=text, **kwargs)

    @safe_send
    async def send_video_note(self, chat_id: int, video_note, **kwargs):
        return await super().send_video_note(chat_id, video_note=video_note, **kwargs)

    @safe_send
    async def send_video(self, chat_id: int, video, **kwargs):
        return await super().send_video(chat_id, video=video, **kwargs)

    @safe_send
    async def send_photo(self, chat_id: int, photo, **kwargs):
        return await super().send_photo(chat_id, photo=photo, **kwargs)

    @safe_send
    async def send_document(self, chat_id: int, document, **kwargs):
        return await super().send_document(chat_id, document=document, **kwargs)

    @safe_send
    async def send_audio(self, chat_id: int, audio, **kwargs):
        return await super().send_audio(chat_id, audio=audio, **kwargs)

    @safe_send
    async def send_animation(self, chat_id: int, animation, **kwargs):
        return await super().send_animation(chat_id, animation=animation, **kwargs)