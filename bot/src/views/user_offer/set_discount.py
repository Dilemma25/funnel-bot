from src.models import UserOffer
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


async def set_discount(
        user_id: int,
        offer_code: str,
        discount_price: float,
        discount_duration,
        connection
):
    """
    Установить скидку для конкретного оффера юзера

    Args:
        user_id: ID пользователя
        offer_code: Код оффера (например, "SMART_WALLET")
        discount_price: Цена со скидкой
        discount_duration_seconds: Длительность скидки в секундах
        connection: Опциональное подключение для транзакции
    """

    expires_at = datetime.now() + discount_duration

    # Получаем UserOffer
    user_offer = await UserOffer.filter(
        user_id=user_id,
        offer__code=offer_code
    ).using_db(connection).first()

    if not user_offer:
        raise ValueError(f"UserOffer не найден для user_id={user_id}, offer_code={offer_code}")

    # Обновляем скидку
    user_offer.discount_price = discount_price
    user_offer.discount_expires_at = expires_at

    await user_offer.save(using_db=connection)

    logger.info(f"✅ Скидка установлена для user_id={user_id}, offer={offer_code}: {discount_price} ₽ до {expires_at}")

    return user_offer