from aiogram import Router

from src.views.tasks import create_task

from datetime import datetime
from datetime import timedelta
from datetime import timezone

from aiogram.types import Message

echo_router = Router()

# @echo_router.message()
# async def echo_handler(message: Message) -> None:
#     try:
#
#         task_type = "send_message"
#
#         payload = {
#             "user_id": message.from_user.id,
#             "text": message.text,
#         }
#
#         time_run = datetime.now(timezone.utc) + timedelta(seconds=70)
#
#         await create(message.from_user.id, task_type, payload, time_run)
#     except Exception as e:
#         print(e)
#         await message.answer(f"Nice try!, {e}")