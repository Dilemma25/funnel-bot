from tortoise.models import Model
from tortoise import fields

class UserRoleEnum:
    ADMIN = 'admin'
    USER = 'user'

# TODO скорее всего прийдется добавить поле, что пользователь не активен, надо будет подумать
class User(Model):
    telegram_id = fields.BigIntField(pk=True)

    role = fields.CharField(max_length=100, default=UserRoleEnum.USER)

    is_message_blocked = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "users"