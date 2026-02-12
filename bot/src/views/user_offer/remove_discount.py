from src.core.config import config
from src.models import UserOffer
from datetime import datetime
import logging
from datetime import timezone


logger = logging.getLogger(__name__)


async def remove_discount(
        user_id: int,
        offer_code: str,
        connection=None
):
    """
    Убрать скидку для конкретного оффера

    Убирает только если скидка ещё активна (не истекла)
    """

    query = UserOffer.filter(user_id=user_id, offer__code=offer_code)

    if connection:
        query = query.using_db(connection)

    user_offer = await query.first()

    if not user_offer:
        logger.warning(f"UserOffer не найден для user_id={user_id}, offer={offer_code}")
        return

    now = datetime.now(config["TIMEZONE"])

    discount_expires = user_offer.discount_expires_at
    if discount_expires and discount_expires.tzinfo is None:
        # Если naive — добавь timezone
        discount_expires = discount_expires.replace(tzinfo=config["TIMEZONE"])

    # Проверяем, есть ли активная скидка
    if (
            user_offer.discount_price is not None and
            user_offer.discount_expires_at and
            user_offer.discount_expires_at.replace(tzinfo=config["TIMEZONE"]) > now
    ):
        user_offer.discount_price = None
        user_offer.discount_expires_at = None

        if connection:
            await user_offer.save(using_db=connection)
        else:
            await user_offer.save()

        logger.info(f"✅ Скидка убрана для user_id={user_id}, offer={offer_code}")
    else:
        logger.info(f"ℹ️ Скидка уже неактивна для user_id={user_id}, offer={offer_code}")