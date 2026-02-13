from tortoise import fields
from tortoise.models import Model


class PaymentStatusEnum:
    PENDING = 'PENDING'
    SUCCESSFUL = 'SUCCESSFUL'
    CANCELED = 'CANCELED'
    FAILED = 'FAILED'


class UserOfferPayment(Model):
    id = fields.BigIntField(pk=True)

    # ЮKassa данные
    yookassa_payment_id = fields.CharField(max_length=300, unique=True)
    yookassa_payment_url = fields.CharField(max_length=300)

    user = fields.ForeignKeyField(
        "models.User",
        related_name="payments",
        on_delete=fields.CASCADE
    )

    offer = fields.ForeignKeyField(
        "models.Offer",
        related_name="payments",
        on_delete=fields.CASCADE
    )

    # Данные платежа
    amount = fields.FloatField()
    status = fields.CharField(max_length=30, default=PaymentStatusEnum.PENDING)

    # Timestamps
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "user_offer_payments"
