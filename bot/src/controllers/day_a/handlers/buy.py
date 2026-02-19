from datetime import datetime, timezone, timedelta

from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup
from tortoise.transactions import in_transaction

from src.models.payment import PaymentStatusEnum
from src.models.sent_message import SentMessageTagEnum, SentMessageDeleteTimings
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
from src.controllers.common_states import CommonStates


@day_a_router.callback_query(F.data.contains(":buy"))
async def handle_buy(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    user_id = callback.from_user.id

    payload = {
        "clicked_button": f"{callback.data.split(":")[1]}: Оплата({callback.data.split(":")[1].capitalize().replace("_", ".")})"
    }

    await create_user_history(
        user_id=user_id,
        event_type=EventTypeEnum.BUTTON_CLICKED,
        user_stage=DayAStates.A_9_2_FAQ_SENT,
        payload=payload,
    )

    payment_lock_until_ts = await state.get_value("payment_lock_until_ts")

    # Получаем актуальную цену
    current_price = await get_current_price(user_id, OfferCodesEnum.SMART_WALLET)

    #TODO Сделать что бы бот выл впринципе не активен на команды после оплаты, тк он должен перейти уже к курсу
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
        payment_status=PaymentStatusEnum.PENDING,
        order_by="newest",
    )

    if not pending_payment or pending_payment.amount != current_price:
        # Создаем платеж в ЮKassa
        payment_data = await PaymentService.create_payment(
            user_id=user_id,
            amount=current_price,
            description="Курс 'Метод умного кошелька'"
        )

        payment_lock_until_ts = None

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
        payment_id = pending_payment.id
        payment_url = pending_payment.yookassa_payment_url

    payment_lock_until = datetime.fromtimestamp(payment_lock_until_ts, timezone.utc) if payment_lock_until_ts else None

    if payment_lock_until and payment_lock_until > datetime.now(timezone.utc):
        await callback.answer(
            text="Сообщение для перехода к оплате уже создано",
            show_alert=False
        )

        return

    elif not payment_lock_until or payment_lock_until < datetime.now(timezone.utc):
        until_timestamp = int((datetime.now(timezone.utc) + timedelta(minutes=15)).timestamp())

        await state.update_data(
            payment_lock_until_ts=until_timestamp,
        )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Оплатить", url=payment_url)],
    ])

    message = await callback.message.answer(
        text=f"💰 К оплате: {current_price} ₽\n\n"
             f"Нажми кнопку ниже для перехода к оплате.\n",
        reply_markup=keyboard
    )

    async with in_transaction() as conn:
        await track_message(
            user_id=user_id,
            tag=SentMessageTagEnum.FUNNEL,
            telegram_message_id=message.message_id,
            stage=DayAStates.PAYMENT_PROCESS,

            delete_at=datetime.now(settings.timezone) + SentMessageDeleteTimings.get_short(),
            delete_on_stage=CommonStates.DISCOUNT_EXPIRES,
            connection=conn
        )

        await update_user_state(
            user_id=user_id,
            offer_code=OfferCodesEnum.SMART_WALLET,
            state=DayAStates.PAYMENT_PROCESS,
            last_activity_at=datetime.now(settings.timezone),
            connection=conn
        )
