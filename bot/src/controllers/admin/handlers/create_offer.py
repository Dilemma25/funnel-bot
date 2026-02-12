from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from src.states.admin import AdminStates
from src.views.offer import create_offer
from . import admin_router


@admin_router.callback_query(F.data == "admin_create_offer")
async def start_create_offer(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    await callback.message.answer(
        "📝 Создание нового оффера\n\n"
        "Отправь данные в формате:\n"
        "<code>code|title|description|base_price</code>\n\n"
        "Пример:\n"
        "<code>ADVANCED_WALLET|Продвинутый кошелёк|Курс про инвестиции|5990</code>",
        parse_mode="HTML"
    )

    await state.set_state(AdminStates.waiting_for_offer_data)


@admin_router.message(AdminStates.waiting_for_offer_data)
async def receive_offer_data(message: Message, state: FSMContext):
    if not message.text or "|" not in message.text:
        await message.answer("❌ Неверный формат. Используй: code|title|description|price")
        return

    try:
        parts = message.text.split("|")
        if len(parts) != 4:
            raise ValueError("Нужно 4 части")

        code, title, description, price_str = parts
        base_price = float(price_str.strip())

        offer = await create_offer(
            code=code.strip(),
            title=title.strip(),
            description=description.strip(),
            base_price=base_price
        )

        await message.answer(
            f"✅ Оффер создан!\n\n"
            f"🆔 ID: {offer.id}\n"
            f"📌 Code: <code>{offer.code}</code>\n"
            f"📝 Название: {offer.title}\n"
            f"💰 Цена: {offer.base_price} ₽",
            parse_mode="HTML"
        )

    except Exception as e:
        await message.answer(f"❌ Ошибка: {str(e)}")

    await state.clear()