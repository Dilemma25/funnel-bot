from src.models import UserOffer, Offer
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


async def get_current_price(user_id: int, offer_code: str, connection) -> float:
    """
    Получить актуальную цену для юзера по конкретному офферу

    Логика:
    - Если есть активная скидка → discount_price
    - Иначе → base_price оффера

    Returns:
        Актуальная цена в рублях
    """

    # Получаем UserOffer с оффером
    user_offer = await UserOffer.filter(
        user_id=user_id,
        offer__code=offer_code
    ).using_db(connection).prefetch_related("offer").first()

    if not user_offer:
        # Если UserOffer нет, берём базовую цену из оффера
        offer = await Offer.get(code=offer_code)
        logger.info(f"UserOffer не найден, возвращаем базовую цену: {offer.base_price} ₽")
        return offer.base_price

    # Проверяем активность скидки
    if (
            user_offer.discount_price is not None and
            user_offer.discount_expires_at and
            user_offer.discount_expires_at > datetime.now()
    ):
        logger.info(f"Активная скидка: {user_offer.discount_price} ₽")
        return user_offer.discount_price
    else:
        logger.info(f"Скидка неактивна, базовая цена: {user_offer.offer.base_price} ₽")
        return user_offer.offer.base_price


async def is_discount_active(user_id: int, offer_code: str) -> bool:
    """Проверить, активна ли скидка"""

    user_offer = await UserOffer.filter(
        user_id=user_id,
        offer__code=offer_code
    ).first()

    if not user_offer:
        return False

    return (
            user_offer.discount_price is not None and
            user_offer.discount_expires_at and
            user_offer.discount_expires_at > datetime.now()
    )