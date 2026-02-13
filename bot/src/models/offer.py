from tortoise.models import Model
from tortoise import fields


class OfferCodesEnum:
    SMART_WALLET = "SMART_WALLET"


class Offer(Model):
    id = fields.IntField(pk=True)

    code = fields.CharField(max_length=50, unique=True) #идентификатор курса
    title = fields.CharField(max_length=255) # название курса
    description = fields.TextField(null=True) # по желанию, краткое обьяснение

    base_price = fields.FloatField()  # цена в рублях.копейках

    class Meta:
        table = "offers"