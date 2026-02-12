from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup
from aiogram.filters import Command
from tortoise.transactions import in_transaction

from src.models.payment import PaymentStatusEnum
from src.views.user_offer_payment import create_user_offer_payment
from . import day_a_router
from src.services.payment import PaymentService
from src.states.day_a import DayAStates
from src.views.user_offer import get_current_price
from src.models.offer import OfferCodesEnum
from src.views.user_offer import get_user_offer
from src.views.user_offer_payment import mark_payment
from src.views.user_offer_payment import get_successful_payment
from src.core.config import config

from datetime import datetime


@day_a_router.callback_query(F.data.contains(":buy"))
@day_a_router.message(Command("buy"))
async def handle_buy(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    # await callback.message.edit_reply_markup(reply_markup=None)

    user_id = callback.from_user.id

    # Получаем актуальную цену
    current_price = await get_current_price(user_id, OfferCodesEnum.SMART_WALLET)

    data = await state.get_data()
    # Получаем из редиса или pg урл платежа и его время
    payment_url = data.get("payment_url")
    payment_created_at = data.get("payment_created_at")
    payment_price = data.get("payment_price")

    # если платежа еще не существует или если платеж старше 10ти минут, мы дадим создать новый,
    # иначе используем старую ссылку
    #TODO перевести в переменную валидную длительность жизни платежа
    if (
            not payment_url or
        (
            payment_price and
            payment_price != current_price
        ) or
        (
            payment_created_at and
            (datetime.now(config["TIMEZONE"]) - datetime.fromisoformat(payment_created_at.replace("Z", "+00:00"))).total_seconds() > 60)
        ):
        # Создаем платеж в ЮKassa
        payment_data = await PaymentService.create_payment(
            user_id=user_id,
            amount=current_price,
            description="Курс 'Метод умного кошелька'"
        )

        payment_id = payment_data["payment_id"]
        payment_url = payment_data["confirmation_url"]
        payment_created_at = payment_data["created_at"]

        await state.update_data(
            payment_url = payment_url,
            payment_created_at = payment_created_at,
        )

        async with in_transaction() as conn:

            user_offer = await get_user_offer(
                user_id=user_id,
                offer_code=OfferCodesEnum.SMART_WALLET,
                connection=conn
            )

            if not user_offer:
                return

            existing_payment = await get_successful_payment(user_offer.id, conn)
            if existing_payment:
                await callback.message.answer("✅ Ты уже купил этот курс!")
                return

            await create_user_offer_payment(
                user_offer_id=user_offer.id,
                yookassa_payment_id=payment_id,
                amount=current_price,
                connection=conn
            )

    #TODO тестовая, убрать кнопку "я оплатил"
    # Отправляем ссылку на оплату
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Оплатить", url=payment_url)],
        [InlineKeyboardButton(text="✅ Я оплатил", callback_data=f"check:")],
    ])

    await callback.message.answer(
        text=f"💰 К оплате: {current_price} ₽\n\n"
        f"Нажми кнопку ниже для перехода к оплате.\n"
        f"После оплаты вернись сюда и нажми 'Я оплатил'.",
        reply_markup=keyboard
    )

    await state.set_state(DayAStates.day_a_10_payment_process)


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

        return

    async with in_transaction() as conn:

        await mark_payment(
            payment_id=payment_id,
            new_status=PaymentStatusEnum.SUCCESSFUL,
            connection=conn,
        )

    await callback.answer("✅ Оплата подтверждена!", show_alert=True)

    await callback.message.answer(
        "🎉 Добро пожаловать на курс!\n\n"
        "Доступ открыт."
    )
