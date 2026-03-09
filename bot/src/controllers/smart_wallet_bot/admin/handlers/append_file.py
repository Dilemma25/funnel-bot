from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types import CallbackQuery

from src.models.media import BotTagEnum, MediaFileTypeEnum
from src.states.admin import AdminStates
from src.views.media import save_media
from src.views.offer import get_offer_by_code
from src.models.offer import OfferCodesEnum
from src.controllers.smart_wallet_bot.admin.handlers.admin_menu import admin_menu

from . import admin_router


@admin_router.callback_query(F.data.startswith("admin_add_file"))
async def offer_selected(callback: CallbackQuery, state: FSMContext):
    """Шаг 2: Оффер выбран, запрашиваем файл"""
    await callback.answer()

    offer = await get_offer_by_code(OfferCodesEnum.SMART_WALLET)
    # Сохраняем в state
    await state.update_data(
        selected_offer_id=offer.id,
        selected_offer_code=offer.code
    )

    await callback.message.answer(
        text=(
        f"📁 Теперь отправь файл (видео, PDF, изображение или видео-кружок)"
        f"Чтобы прекратить добавлять файлы, введите команду /close"
              ),
        parse_mode="HTML"
    )

    await state.set_state(AdminStates.waiting_for_file)

@admin_router.message(Command("close"))
async def handle_close(message: Message, state: FSMContext):
    await state.clear()

    await admin_menu(
        message=message,
        state=state
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

    await state.update_data(
        file_id=file_id,
        file_type=file_type,
    )

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
            bot_tag=BotTagEnum.SMART_WALLET_COURSE,
            file_type=file_type,
        )

        await message.answer(
            f"✅ Файл сохранён!\n\n"
            f"📄 Код файла: <code>{file_code}</code>\n"
            f"🆔 File ID: <code>{file_id[:20]}...</code>"
            f" Тип файла: <code>{file_type}...</code>",
            parse_mode="HTML"
        )

    except Exception as e:
        await message.answer(f"❌ Ошибка: {str(e)}")

    await state.set_state(AdminStates.waiting_for_file)