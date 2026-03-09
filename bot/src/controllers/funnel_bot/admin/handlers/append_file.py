from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton

from src.models import Offer
from src.models.media import BotTagEnum, MediaFileTypeEnum
from src.states.admin import AdminStates
from src.views.media import save_media
from . import admin_router
from .admin_menu import admin_menu


@admin_router.callback_query(F.data == "admin_add_file")
async def choose_offer_for_file(callback: CallbackQuery, state: FSMContext):
    """Шаг 1: Выбор оффера"""
    await callback.answer()

    # Получаем все офферы
    offers = await Offer.all()

    if not offers:
        await callback.message.answer(
            "❌ Сначала создай хотя бы один оффер!\n"
            "Используй команду /admin → Создать оффер"
        )
        return

    # Создаём кнопки для каждого оффера
    buttons = []
    for offer in offers:
        buttons.append([
            InlineKeyboardButton(
                text=f"{offer.title} ({offer.code})",
                callback_data=f"admin_select_offer:{offer.id}"
            )
        ])

    # Кнопка "Назад"
    buttons.append([
        InlineKeyboardButton(text="◀️ Назад", callback_data="admin_back")
    ])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await callback.message.answer(
        "📦 Выбери оффер, в который добавить файл:",
        reply_markup=keyboard
    )

    await state.set_state(AdminStates.waiting_for_offer_selection)


@admin_router.callback_query(F.data.startswith("admin_select_offer:"))
async def offer_selected(callback: CallbackQuery, state: FSMContext):
    """Шаг 2: Оффер выбран, запрашиваем файл"""
    await callback.answer()

    # Извлекаем offer_code из callback_data
    offer_id = callback.data.split(":")[1]
    offer = await Offer.filter(id=offer_id).first()
    # Сохраняем в state
    await state.update_data(
        selected_offer_id=offer_id,
        selected_offer_code=offer.code
    )

    await callback.message.answer(
        text=(f"✅ Оффер выбран: <b>{offer.code}</b>\n\n"
        "📁 Теперь отправь файл (видео, PDF, изображение или видео-кружок)"
        "Чтобы прекратить добавлять файлы, введите команду /close"
              ),
        parse_mode="HTML"
    )

    await state.set_state(AdminStates.waiting_for_file)

@admin_router.message(Command("close"))
async def handle_close(message: Message, state: FSMContext):
    await state.clear()

    await admin_menu(
        message=message,
        state=state,
    )

@admin_router.message(AdminStates.waiting_for_file)
async def receive_file(message: Message, state: FSMContext):
    """Шаг 3: Получаем файл"""
    file_id = None
    file_type = None

    if message.video:
        file_id = message.video.file_id
        file_type = MediaFileTypeEnum.VIDEO
    elif message.document:
        file_id = message.document.file_id
        file_type = MediaFileTypeEnum.DOCUMENT
    elif message.video_note:
        file_id = message.video_note.file_id
        file_type = MediaFileTypeEnum.VIDEO_NOTE
    elif message.photo:
        file_id = message.photo[-1].file_id
        file_type = MediaFileTypeEnum.PHOTO
    else:
        await message.answer("❌ Отправь видео, документ, фото или видео-кружок")
        return

    await state.update_data(file_id=file_id)

    await message.answer(
        "✅ Файл получен!\n\n"
        "Теперь отправь <b>код</b> для этого файла (например: <code>test_big</code>, <code>V1_krujok_jadnost</code>)",
        parse_mode="HTML"
    )

    await state.set_state(AdminStates.waiting_for_file_name)


@admin_router.message(AdminStates.waiting_for_file_name)
async def receive_file_code(message: Message, state: FSMContext):
    """Шаг 4: Получаем код файла и сохраняем"""
    if not message.text:
        await message.answer("❌ Отправь текст (код файла)")
        return

    file_code = message.text.strip()

    # Получаем данные из state
    data = await state.get_data()
    file_id = data.get('file_id')
    offer_code = data.get('selected_offer_code')
    offer_id = data.get('selected_offer_id')
    file_type = data.get('file_type')

    try:
        await save_media(
            file_code=file_code,
            file_id=file_id,
            offer_id=offer_id,
            bot_tag=BotTagEnum.FUNNEL,
            file_type=file_type,
        )

        await message.answer(
            f"✅ Файл сохранён!\n\n"
            f"📦 Оффер: <code>{offer_code}</code>\n"
            f"📄 Код файла: <code>{file_code}</code>\n"
            f"🆔 File ID: <code>{file_id[:20]}...</code>"
            f" Тип файла: <code>{file_type}...</code>",
            parse_mode="HTML"
        )

    except Exception as e:
        await message.answer(f"❌ Ошибка: {str(e)}")

    await state.set_state(AdminStates.waiting_for_file)


@admin_router.callback_query(F.data == "admin_back")
async def go_back_to_menu(callback: CallbackQuery, state: FSMContext):
    """Возврат в главное меню"""
    await callback.answer()

    await admin_menu(
        message=callback.message,
        state=state,
    )