from src.models import UserOffer
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


async def remove_discount(
        user_id: int,
        offer_code: str,
        connection
):
    """
    Убрать скидку для конкретного оффера

    Убирает только если скидка ещё активна (не истекла)
    """

    user_offer = await (UserOffer.filter(
        user_id=user_id,
        offer__code=offer_code
    ).using_db(connection).first())

    if not user_offer:
        logger.warning(f"UserOffer не найден для user_id={user_id}, offer={offer_code}")
        return

    # Проверяем, есть ли активная скидка
    if (
            user_offer.discount_price is not None and
            user_offer.discount_expires_at and
            user_offer.discount_expires_at > datetime.now()
    ):
        user_offer.discount_price = None
        user_offer.discount_expires_at = None

        await user_offer.save(using_db=connection)


        logger.info(f"✅ Скидка убрана для user_id={user_id}, offer={offer_code}")
    else:
        logger.info(f"ℹ️ Скидка уже неактивна для user_id={user_id}, offer={offer_code}")