from src.core.config import config
from src.models import UserOffer, Offer
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


async def get_current_price(user_id: int, offer_code: str, connection=None) -> float:
    """
    Получить актуальную цену для юзера по конкретному офферу

    Логика:
    - Если есть активная скидка → discount_price
    - Иначе → base_price оффера

    Returns:
        Актуальная цена в рублях
    """

    # Получаем UserOffer с оффером
    query = UserOffer.filter(user_id=user_id, offer__code=offer_code).prefetch_related("offer")

    if connection:
        query = query.using_db(connection)

    user_offer = await query.first()

    #TODO обработать
    if not user_offer:
        # Если UserOffer нет, берём базовую цену из оффера
        offer_query = Offer.filter(code=offer_code)

        if connection:
            offer_query = offer_query.using_db(connection)

        offer = await offer_query.first()

        logger.info(f"UserOffer не найден, возвращаем базовую цену: {offer.base_price} ₽")
        return offer.base_price

    now = datetime.now(config["TIMEZONE"])
    # Проверяем активность скидки
    if (
            user_offer.discount_price is not None and
            user_offer.discount_expires_at and
            user_offer.discount_expires_at > now
    ):
        logger.info(f"Активная скидка: {user_offer.discount_price} ₽")
        return user_offer.discount_price
    else:
        logger.info(f"Скидка неактивна, базовая цена: {user_offer.offer.base_price} ₽")
        return user_offer.offer.base_price


async def is_discount_active(user_id: int, offer_code: str, connection=None) -> bool:
    """Проверить, активна ли скидка"""

    query = UserOffer.filter(user_id=user_id, offer__code=offer_code)

    if connection:
        query = query.using_db(connection)

    user_offer = await query.first()

    if not user_offer:
        return False

    now = datetime.now(config["TIMEZONE"])

    return (
            user_offer.discount_price is not None and
            user_offer.discount_expires_at and
            user_offer.discount_expires_at > now
    )