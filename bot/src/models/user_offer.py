from tortoise.models import Model
from tortoise import fields

from enum import Enum


class UserOfferStatusEnum(str, Enum):
    ACTIVE = "active"  # Активен, проходит воронку
    PURCHASED = "purchased"  # Купил
    DROPPED = "dropped"  # Отвалился на каком то этапе
    BLOCKED_BOT = "blocked_bot"  # Заблокировал бота
    COMPLETED_FREE = "completed_free"  # Прошёл воронку, но не купил


class UserOffer(Model):
    id = fields.IntField(pk=True)

    user = fields.ForeignKeyField("models.User", related_name="offers", on_delete=fields.CASCADE)
    offer = fields.ForeignKeyField("models.Offer", related_name="user_offers", on_delete=fields.CASCADE)

    discount_price = fields.FloatField(null=True)          # персональная скидка
    discount_expires_at = fields.DatetimeField(null=True)  # срок действия скидки

    status = fields.CharEnumField(
        UserOfferStatusEnum,
        default=UserOfferStatusEnum.ACTIVE
    )

    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "user_offers"
        unique_together = ("user", "offer")