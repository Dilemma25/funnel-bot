from tortoise.models import Model
from tortoise import fields
from datetime import datetime


class UserOffer(Model):
    id = fields.IntField(pk=True)

    user = fields.ForeignKeyField("models.User", related_name="offers", on_delete=fields.CASCADE)
    offer = fields.ForeignKeyField("models.Offer", related_name="user_offers", on_delete=fields.CASCADE)

    discount_price = fields.FloatField(null=True)          # персональная скидка
    discount_expires_at = fields.DatetimeField(null=True) # срок действия скидки

    created_at = fields.DatetimeField(default=datetime.now)

    class Meta:
        table = "user_offers"
        unique_together = ("user", "offer")