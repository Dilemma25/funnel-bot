from src.core.config import config
from src.models import UserOffer
from datetime import datetime, timedelta
import logging

from src.views.user_offer_payment import get_successful_payment


logger = logging.getLogger(__name__)


async def set_discount(
        user_id: int,
        offer_code: str,
        discount_price: float,
        discount_duration: int,
        connection=None
):
    """
    Установить скидку для конкретного оффера юзера

    Args:
        user_id: ID пользователя
        offer_code: Код оффера (например, "SMART_WALLET")
        discount_price: Цена со скидкой
        discount_duration: Длительность скидки в секундах
        connection: Опциональное подключение для транзакции
    """

    expires_at = datetime.now(config["TIMEZONE"]) + timedelta(seconds=discount_duration)

    # Получаем UserOffer
    query = UserOffer.filter(user_id=user_id, offer__code=offer_code)

    if connection:
        query = query.using_db(connection)

    user_offer = await query.first()

    if not user_offer:
        raise ValueError(f"UserOffer не найден для user_id={user_id}, offer_code={offer_code}")

    successful_payment = await get_successful_payment(user_offer.id, connection)

    if successful_payment:
        return None


    # Обновляем скидку
    user_offer.discount_price = discount_price
    user_offer.discount_expires_at = expires_at

    if connection:
        await user_offer.save(using_db=connection)
    else:
        await user_offer.save()

    logger.info(f"✅ Скидка установлена для user_id={user_id}, offer={offer_code}: {discount_price} ₽ до {expires_at}")

    return user_offer