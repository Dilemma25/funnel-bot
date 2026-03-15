from tortoise.transactions import in_transaction

from src.models import Offer, UserOffer
from src.models.offer import OfferCodesEnum
from src.models.user_offer import UserOfferStatusEnum
from src.views.tasks.cancel_user_tasks import cancel_user_tasks
from src.views.user import deactivate_user

#TODO прокинуть эту функцию на завершение воронки, и на успешный платеж
async def cancel_user_offer_with_status(
        user_id: int,
        offer_code: str,
        new_status: str,
        connection=None
):
    offer = await Offer.filter(code=offer_code).first()

    if not offer:
        raise ValueError(f"Offer {offer_code} not found")

    async def _execute(conn):
        if new_status == UserOfferStatusEnum.BLOCKED_BOT:
            await deactivate_user(user_id, conn)

        await UserOffer.filter(
            user_id=user_id,
            offer_id=offer.id,
        ).using_db(conn).update(status=new_status)

        await cancel_user_tasks(user_id, conn)

    if connection:
        await _execute(connection)
    else:
        async with in_transaction() as transaction:
            await _execute(transaction)
