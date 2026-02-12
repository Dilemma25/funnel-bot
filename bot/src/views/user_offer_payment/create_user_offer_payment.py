from src.models import UserOfferPayment
from src.models.payment import PaymentStatusEnum


async def create_user_offer_payment(yookassa_payment_id: str, user_offer_id: int, amount: float, connection=None):
    if connection:
        payment = await UserOfferPayment.create(
            yookassa_payment_id = yookassa_payment_id,
            user_offer_id=user_offer_id,
            amount=amount,
            status=PaymentStatusEnum.PENDING,
            using_db=connection,
        )
    else:
        payment = await UserOfferPayment.create(
            yookassa_payment_id = yookassa_payment_id,
            user_offer_id=user_offer_id,
            amount=amount,
            status=PaymentStatusEnum.PENDING,
        )

    return payment