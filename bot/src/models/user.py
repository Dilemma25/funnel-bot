from tortoise.models import Model
from tortoise import fields


# TODO скорее всего прийдется добавить поле, что пользователь не активен, надо будет подумать
class User(Model):
    telegram_id = fields.BigIntField(pk=True)

    is_message_blocked = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "users"