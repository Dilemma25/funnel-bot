from src.models import UserOffer, Offer
from src.models.user_offer import UserOfferStatusEnum
from src.models.offer import OfferCodesEnum
from datetime import datetime
from src.core.config import settings


async def change_user_offer_status(
        user_id: int,
        new_status: UserOfferStatusEnum,
        connection=None
):
    """
    Изменить статус user_offer

    Args:
        user_id: Telegram ID пользователя
        new_status: Новый статус
        connection: DB connection (optional)
    """

    # Сначала найди offer_id
    offer = await Offer.filter(code=OfferCodesEnum.SMART_WALLET).first()

    if not offer:
        raise ValueError(f"Offer {OfferCodesEnum.SMART_WALLET} not found")

    update_data = {
        "status": new_status,
    }

    if connection:
        await UserOffer.filter(
            user_id=user_id,
            offer_id=offer.id,
        ).using_db(connection).update(**update_data)
    else:
        await UserOffer.filter(
            user_id=user_id,
            offer_id=offer.id,
        ).update(**update_data)