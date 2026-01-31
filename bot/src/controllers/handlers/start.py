from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram import Router


start_router = Router()

@start_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {message.from_user.full_name}!")