from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram import Router


start_router = Router()

# @start_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.reply_video(
        video='https://storage.radabot.ru/test/JOPORN_NET_45253_720p.mp4?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=admin%2F20260131%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20260131T204611Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=9f827540946f14a3475148a937a9e9970b3404175b0c8a22cc8b53d509c0a1a4',
        protect_content=True
        )
    await message.answer(f"Hello, {message.from_user.full_name}!")

