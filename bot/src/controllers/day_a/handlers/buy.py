from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import Message
from aiogram.filters import Command
from tortoise.transactions import in_transaction

from src.views.user_offer_payment import create_user_offer_payment
from . import day_a_router
from src.services.payment import PaymentService
from src.states.day_a import DayAStates
from src.views.user_offer import get_current_price
from src.models.offer import OfferCodesEnum
from src.views.user_offer import get_user_offer
from src.views.user_offer_payment import mark_as_successful

@day_a_router.callback_query(F.data.contains(":buy"))
# @day_a_router.message(Command("buy"))
async def handle_buy(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)
    #
    # await callback.message.answer("PLACEHOLDER")

    user_id = callback.from_user.id

    # # Получаем актуальную цену
    async with in_transaction() as conn:
        price = await get_current_price(user_id, OfferCodesEnum.SMART_WALLET, conn)

    # Создаем платеж в ЮKassa
    payment_data = await PaymentService.create_payment(
        user_id=user_id,
        amount=price,
        description="Курс 'Метод умного кошелька'"
    )

    payment_id = payment_data["payment_id"]

    async with in_transaction() as conn:
        user_id = callback.from_user.id

        user_offer = await get_user_offer(
            user_id=user_id,
            offer_code=OfferCodesEnum.SMART_WALLET,
            connection=conn
        )

        await create_user_offer_payment(
            user_offer_id=user_offer.id,
            payment_id=payment_id,
            amount=price,
            connection=conn
        )

    #TODO тестовая, убрать кнопку "я оплатил"
    # Отправляем ссылку на оплату
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Оплатить", url=payment_data["confirmation_url"])],
        [InlineKeyboardButton(text="✅ Я оплатил", callback_data=f"check:{payment_data['payment_id']}")],
    ])

    await callback.message.answer(
        text=f"💰 К оплате: {price} ₽\n\n"
        f"Нажми кнопку ниже для перехода к оплате.\n"
        f"После оплаты вернись сюда и нажми 'Я оплатил'.",
        reply_markup=keyboard
    )

    await state.set_state(DayAStates.day_a_10_payment_process)

# @day_a_router.message(Command("buy"))
# async def handle_buy(message: Message, state: FSMContext):
#     # await callback.answer()
#     # await callback.message.edit_reply_markup(reply_markup=None)
#     #
#     # await callback.message.answer("PLACEHOLDER")
#
#     user_id = message.from_user.id
#     #
#     # # Получаем актуальную цену
#     # price = await get_current_price(user_id)
#
#     price = 2500
#
#     # Создаем платеж в ЮKassa
#     payment_data = await PaymentService.create_payment(
#         user_id=user_id,
#         amount=price,
#         description="Курс 'Метод умного кошелька'"
#     )
#
#     # Сохраняем платеж в БД (опционально)
#     # await PaymentRecord.create(
#     #     user_id=user_id,
#     #     payment_id=payment_data["payment_id"],
#     #     amount=price,
#     #     status="pending"
#     # )
#
#     # Отправляем ссылку на оплату
#     keyboard = InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text="💳 Оплатить", url=payment_data["confirmation_url"])],
#         [InlineKeyboardButton(text="✅ Я оплатил", callback_data=f"check:{payment_data['payment_id']}")],
#     ])
#
#     await message.answer(
#         text=f"💰 К оплате: {price} ₽\n\n"
#         f"Нажми кнопку ниже для перехода к оплате.\n"
#         f"После оплаты вернись сюда и нажми 'Я оплатил'.",
#         reply_markup=keyboard
#     )
#
#     # await state.set_state(DayAStates.day_a_waiting_payment)

#TODO Тестовый хендлер, убрать
@day_a_router.callback_query(F.data.startswith("check:"))
async def check_payment_status_handler(callback: CallbackQuery):
    payment_id = callback.data.split(":")[1]

    # Проверяем статус
    payment_status = await PaymentService.check_payment_status(payment_id)

    if not payment_status["paid"]:

        await callback.answer(
            "⏳ Оплата еще не поступила.\n"
            "Попробуй через минуту.",
            show_alert=True
        )

    async with in_transaction() as conn:

        await mark_as_successful(
            payment_id=payment_id,
            connection=conn,
        )

    await callback.answer("✅ Оплата подтверждена!", show_alert=True)

    await callback.message.answer(
        "🎉 Добро пожаловать на курс!\n\n"
        "Доступ открыт."
    )
