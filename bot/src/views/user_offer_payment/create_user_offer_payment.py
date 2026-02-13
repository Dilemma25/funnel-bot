from src.models import Offer
from src.models.payment import PaymentStatusEnum
from src.models import UserOfferPayment


async def create_user_offer_payment(
        yookassa_payment_id: str,
        yookassa_payment_url: str,
        user_id: int,
        offer_code: str,
        amount: float,
        connection=None
):
    if connection:
        # Получаем offer_id по коду
        offer = await Offer.filter(code=offer_code).using_db(connection).first()
    else:
        offer = await Offer.filter(code=offer_code).first()


    if not offer:
        raise ValueError(f"Offer {offer_code} not found")

    if connection:
        payment = await UserOfferPayment.create(
                yookassa_payment_id = yookassa_payment_id,
                yookassa_payment_url = yookassa_payment_url,
                user_id = user_id,
                offer_id=offer.id,
                amount=amount,
                status=PaymentStatusEnum.PENDING,
                using_db=connection,
            )
    else:
        payment = await UserOfferPayment.create(
            yookassa_payment_id = yookassa_payment_id,
            yookassa_payment_url=yookassa_payment_url,
            user_id = user_id,
            offer_id=offer.id,
            amount=amount,
            status=PaymentStatusEnum.PENDING,
        )

    return payment