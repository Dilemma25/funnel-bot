from datetime import datetime

from aiogram.filters import Command

from src.core.logging_config import setup_logging
from src.views.offer import get_offer_by_code

logger = setup_logging(__name__, service="bot")

from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import Message
from tortoise.transactions import in_transaction

from src.models.payment import PaymentStatusEnum
from src.models.sent_message import SentMessageTagEnum
from src.models.sent_message import SentMessageDeleteTimings
from src.models.user_history import EventTypeEnum
from src.views.sent_message import track_message
from src.views.user_history import create_user_history
from src.views.user_offer_payment import create_user_offer_payment
from src.views.user_state.update_user_state import update_user_state
from . import day_a_router
from src.services.payment import PaymentService
from src.views.user_offer import get_current_price
from src.models.offer import OfferCodesEnum
from src.views.user_offer_payment import get_payment_with_status
from src.controllers.user_states import DayAStates
from src.core.config import settings
from src.states.buy import BuyStates
from src.views.user import get_user


@day_a_router.callback_query(F.data.contains(":buy"))
async def handle_buy(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    user_id = callback.from_user.id

    existing_successful_payment = await get_payment_with_status(
        user_id=user_id,
        offer_code=OfferCodesEnum.SMART_WALLET,
        payment_status=PaymentStatusEnum.SUCCESSFUL
    )

    if existing_successful_payment:
        await callback.message.answer("✅ Ты уже купил этот курс!")
        return

    payload = {
        "clicked_button": f"{callback.data.split(":")[1]}: Оплата({callback.data.split(":")[1].capitalize().replace("_", ".")})"
    }

    await create_user_history(
        user_id=user_id,
        event_type=EventTypeEnum.BUTTON_CLICKED,
        user_stage=DayAStates.A_9_2_FAQ_SENT,
        payload=payload,
    )

    user = await get_user(user_id)

    if user.email is None:
        # Запрашиваем email
        await callback.message.answer(
            "📧 **Укажите email для получения чека**\n\n"
                "После успешной оплаты на указанный адрес будет отправлен официальный чек от ЮKassa.\n\n"
                "Пример: `user@example.com`",
                parse_mode="Markdown"
        )

        await state.set_state(BuyStates.waiting_for_email)
        return

    await create_and_send_payment(
        callback=callback,
        user_email=user.email,
        user_id = user_id,
    )


@day_a_router.message(BuyStates.waiting_for_email, F.text)
async def receive_email(message: Message, state: FSMContext):
    """Получаем email от юзера"""

    user_id = message.from_user.id
    email = message.text.strip()

    # Валидация email
    import re
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if not re.match(email_pattern, email):
        await message.answer(
            "❌ Неправильный формат email.\n\n"
            "Попробуй ещё раз или введи /close для отмены оплаты"
        )
        return

    user = await get_user(user_id=user_id)
    user.email = email
    await user.save()

    await message.answer(f"✅ Email сохранён: `{email}`", parse_mode="Markdown")

    await state.clear()

    await create_and_send_payment(
        user_email=user.email,
        user_id=user_id,
        message=message
    )


@day_a_router.message(BuyStates.waiting_for_email, Command("close"))
async def handle_close(message: Message, state: FSMContext):
    await message.answer("Отмена платежа")

    await state.clear()

async def create_and_send_payment(
    user_id: int,
    user_email: str,
    callback: CallbackQuery=None,
    message: Message=None,
):
    # Получаем актуальную цену
    current_price = await get_current_price(user_id, OfferCodesEnum.SMART_WALLET)

    pending_payment = await get_payment_with_status(
        user_id=user_id,
        offer_code=OfferCodesEnum.SMART_WALLET,
        payment_status=PaymentStatusEnum.PENDING,
        order_by="newest",
    )

    if not pending_payment or pending_payment.amount != current_price:

        offer = await get_offer_by_code(
            code=OfferCodesEnum.SMART_WALLET,
        )
        # Создаем платеж в ЮKassa
        payment_data = await PaymentService.create_payment(
            user_id=user_id,
            user_email=user_email,
            amount=current_price,
            description=offer.title
        )

        if not payment_data:
            logger.critical("Ошибка создания платежа")
            target = callback.message if callback else message
            await target.answer("❌ Не удалось создать платёж. Попробуй позже.")
            return

        payment_id = payment_data["payment_id"]
        payment_url = payment_data["confirmation_url"]

        await create_user_offer_payment(
            user_id=user_id,
            offer_code=OfferCodesEnum.SMART_WALLET,
            yookassa_payment_url=payment_url,
            yookassa_payment_id=payment_id,
            amount=current_price,
        )

    else:
        payment_url = pending_payment.yookassa_payment_url

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Оплатить", url=payment_url)],
    ])

    target = callback.message if callback else message

    #TODO расширить сообщение
    sent_message = await target.answer(
        text=f"💰 К оплате: {current_price} ₽\n\n"
             f"📧 Чек будет отправлен на: `{user_email}`\n\n"
             f"Нажми кнопку ниже для перехода к оплате.\n\n"
             f"Если платеж не будет подтвержден в течение 20 минут\n"
             f"Введите команду /help и напишите обращение в поддержку",
        reply_markup=keyboard
    )

    async with in_transaction() as conn:
        await track_message(
            user_id=user_id,
            tag=SentMessageTagEnum.FUNNEL,
            telegram_message_id=sent_message.message_id,
            stage=DayAStates.PAYMENT_PROCESS,

            delete_at=datetime.now(settings.timezone) + SentMessageDeleteTimings.get_short(),
            delete_on_stage=DayAStates.FINAL,
            connection=conn
        )

        await update_user_state(
            user_id=user_id,
            offer_code=OfferCodesEnum.SMART_WALLET,
            state=DayAStates.PAYMENT_PROCESS,
            last_activity_at=datetime.now(settings.timezone),
            connection=conn
        )
