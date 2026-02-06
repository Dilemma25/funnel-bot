from src.models import UserOfferPayment
from src.models.payment import PaymentStatusEnum


async def create_user_offer_payment(payment_id: str, user_offer_id: int, amount: float, connection):
    payment = await UserOfferPayment.create(
        id=payment_id,
        user_offer_id=user_offer_id,
        amount=amount,
        status=PaymentStatusEnum.PENDING,
        using_db=connection,
    )
    return payment