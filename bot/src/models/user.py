from tortoise.models import Model
from tortoise import fields
from datetime import datetime


# TODO надо обработать чтоб пользователь не начал воронку заново
# TODO скорее всего прийдется добавить поле, что пользователь не активен, надо будет подумать
class User(Model):
    telegram_id = fields.BigIntField(pk=True)

    is_message_blocked = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(default=datetime.now)

    class Meta:
        table = "users"