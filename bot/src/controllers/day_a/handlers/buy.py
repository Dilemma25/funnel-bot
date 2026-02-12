from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup
from aiogram.filters import Command

from src.models.payment import PaymentStatusEnum
from src.views.user_offer_payment import create_user_offer_payment
from src.views.user_state.update_user_state import update_user_state
from . import day_a_router
from src.services.payment import PaymentService
from src.views.user_offer import get_current_price
from src.models.offer import OfferCodesEnum
from src.views.user_offer_payment import get_payment_with_status
from src.core.config import settings

from datetime import datetime

from ..user_states import DayAStates


@day_a_router.callback_query(F.data.contains(":buy"))
@day_a_router.message(Command("buy"))
async def handle_buy(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    user_id = callback.from_user.id

    # Получаем актуальную цену
    current_price = await get_current_price(user_id, OfferCodesEnum.SMART_WALLET)

    existing_successful_payment = await get_payment_with_status(
        user_id=user_id,
        offer_code=OfferCodesEnum.SMART_WALLET,
        payment_status=PaymentStatusEnum.SUCCESSFUL
    )

    if existing_successful_payment:
        await callback.message.answer("✅ Ты уже купил этот курс!")
        return

    pending_payment = await get_payment_with_status(
        user_id=user_id,
        offer_code=OfferCodesEnum.SMART_WALLET,
        payment_status=PaymentStatusEnum.PENDING
    )

    payment_id = pending_payment.id
    payment_url = pending_payment.yookassa_payment_url

    if not pending_payment or pending_payment.amount != current_price:
        # Создаем платеж в ЮKassa
        payment_data = await PaymentService.create_payment(
            user_id=user_id,
            amount=current_price,
            description="Курс 'Метод умного кошелька'"
        )

        payment_id = payment_data["payment_id"]
        payment_url = payment_data["confirmation_url"]

        await create_user_offer_payment(
            user_id=user_id,
            offer_code=OfferCodesEnum.SMART_WALLET,
            yookassa_payment_url=payment_url,
            yookassa_payment_id=payment_id,
            amount=current_price,
        )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Оплатить", url=payment_url)],
        # [InlineKeyboardButton(text="✅ Я оплатил", callback_data=f"check:")],
    ])

    await callback.message.answer(
        text=f"💰 К оплате: {current_price} ₽\n\n"
             f"Нажми кнопку ниже для перехода к оплате.\n",
        reply_markup=keyboard
    )

    await update_user_state(
        user_id=user_id,
        offer_code=OfferCodesEnum.SMART_WALLET,
        state=DayAStates.DAY_A_10_PAYMENT_PROCESS,
        last_activity_at=datetime.now(settings.timezone),
    )


# #TODO Тестовый хендлер, убрать
# @day_a_router.callback_query(F.data.startswith("check:"))
# async def check_payment_status_handler(callback: CallbackQuery):
#     payment_id = callback.data.split(":")[1]
#
#     # Проверяем статус
#     payment_status = await PaymentService.check_payment_status(payment_id)
#
#     if not payment_status["paid"]:
#
#         await callback.answer(
#             "⏳ Оплата еще не поступила.\n"
#             "Попробуй через минуту.",
#             show_alert=True
#         )
#
#         return
#
#     async with in_transaction() as conn:
#
#         await mark_payment(
#             payment_id=payment_id,
#             new_status=PaymentStatusEnum.SUCCESSFUL,
#             connection=conn,
#         )
#
#     await callback.answer("✅ Оплата подтверждена!", show_alert=True)
#
#     await callback.message.answer(
#         "🎉 Добро пожаловать на курс!\n\n"
#         "Доступ открыт."
#     )
