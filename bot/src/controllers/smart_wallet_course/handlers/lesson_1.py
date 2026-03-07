import asyncio

from aiogram import F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message

from src.controllers.smart_wallet_course.handlers import smart_wallet_router
from src.models.offer import OfferCodesEnum
from src.views.media import get_media_by_file_code


@smart_wallet_router.callback_query(F.data == "lesson_1")
async def handle_lesson_1(
        callback: CallbackQuery,
):
    """Урок 1: Финансовый рентген"""

    await callback.answer()

    #TODO добавить перечисление file_codes
    video = await get_media_by_file_code(
        offer_code=OfferCodesEnum.SMART_WALLET,
        file_code="lesson_1_module_1_video"
    )

    calculator = await get_media_by_file_code(
        offer_code=OfferCodesEnum.SMART_WALLET,
        file_code="lesson_1_module_1_calculator"
    )

    check_list = await get_media_by_file_code(
        offer_code=OfferCodesEnum.SMART_WALLET,
        file_code="lesson_1_module_1_check_list"
    )


    text = (
        "<i>(Финансовый рентген)</i>\n\n"
        "Ну что, ты только что сделал одну из самых важных вещей —\n"
        "честно посмотрел, куда уходят твои деньги.\n\n"
        "Почти у всех на этом этапе появляется удивление и лёгкий шок.\n"
        "Это нормально.\n\n"
        "Главное — теперь у тебя есть <b>ясность и контроль</b>.\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "<b>После урока тебе доступно:</b>\n"
        "➤ таблица финансового рентгена с автоматическими подсчётами;\n"
        "➤ чек-лист мест, где чаще всего теряются деньги.\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "<b>Что важно сделать сейчас:</b>\n"
        "① заполни таблицу минимум за 30 дней;\n"
        "② найди 5 самых заметных лишних трат;\n"
        "③ отключи хотя бы 2 ненужные подписки.\n\n"
        "Уже этого шага достаточно, чтобы запустить изменения.\n"
        "Но дальше будет ещё интереснее!"
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="▸ Следующий урок(В РАЗРАБОТКЕ)",
            callback_data="lesson_2"
        )]
    ])

    await callback.message.answer_video(
        video=video
    )

    await asyncio.sleep(0.25)

    await callback.message.answer_document(
        document=calculator,
    )

    await asyncio.sleep(0.25)

    await callback.message.answer_document(
        document=check_list,
    )

    await asyncio.sleep(0.25)

    await callback.message.answer(
        text=text,
        parse_mode="HTML",
        reply_markup=keyboard
    )

