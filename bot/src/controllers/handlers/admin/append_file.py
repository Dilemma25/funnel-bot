from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types import CallbackQuery
from src.states.admin import AdminStates
from src.views.media import save_media
from . import admin_router


# @admin_router.message(Command("add_file"))
@admin_router.callback_query(F.data == "admin_add_file")
async def add_file_command(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("📁 Отправь файл (видео, PDF, изображение)")
    await state.set_state(AdminStates.waiting_for_file)
    await callback.answer()

@admin_router.message(AdminStates.waiting_for_file)
async def receive_file(message: Message, state: FSMContext):
    file_id = None

    if message.video:
        file_id = message.video.file_id
    elif message.document:
        file_id = message.document.file_id
    else:
        await message.answer("❌ Отправь видео, документ или фото")
        return

    # Сохрани file_id в контексте
    await state.update_data(file_id=file_id)

    # Попроси названия
    await message.answer("✅ Файл получен!\n\nТеперь отправь названия для этого файла")
    await state.set_state(AdminStates.waiting_for_file_name)


@admin_router.message(AdminStates.waiting_for_file_name)
async def receive_file_name(message: Message, state: FSMContext):
    if not message.text:
        await message.answer("❌ Отправь текст (название файла)")
        return

    name = message.text

    print(name)

    data = await state.get_data()
    file_id = data.get('file_id')

    try:
        await save_media(name, file_id)
        await message.answer(f"✅ Файл '{name}' сохранён в БД")
    except Exception as e:
        print(e)
        await message.answer(f"❌ Ошибка: {str(e)}")

    await state.clear()