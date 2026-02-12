from tortoise import fields
from tortoise.models import Model
from datetime import datetime


class PaymentStatusEnum:
    PENDING = 'PENDING'
    SUCCESSFUL = 'SUCCESSFUL'
    CANCELED = 'CANCELED'
    FAILED = 'FAILED'


#TODO Хранить урд платежа
class UserOfferPayment(Model):
    id = fields.BigIntField(pk=True)
    yookassa_payment_id = fields.CharField(max_length=200)

    user_offer = fields.ForeignKeyField(
        "models.UserOffer",
        related_name="payments",
        on_delete=fields.SET_NULL,
        null=True,
    )

    amount = fields.FloatField()
    status = fields.CharField(max_length=30, default=PaymentStatusEnum.PENDING)
    created_at = fields.DatetimeField(default=datetime.now)

    class Meta:
        table = "user_offer_payments"
