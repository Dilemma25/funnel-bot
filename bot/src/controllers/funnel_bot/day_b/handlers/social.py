from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram import F

import src.controllers.funnel_bot.day_b.messages as messages

from . import day_b_router


@day_b_router.callback_query(F.data == "day_b:b2:full_package")
async def social_handler(callback: CallbackQuery, state: FSMContext):

    await callback.message.edit_reply_markup(reply_markup=None)

    message = await callback.message.answer(
        text=messages.message_B2,
        protect_content=True,
        parse_mode="Markdown",
    )

