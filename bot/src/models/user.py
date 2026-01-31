from tortoise.models import Model
from tortoise import fields
from datetime import datetime


class User(Model):
    telegram_id = fields.BigIntField(pk=True)
    course_paid = fields.BooleanField(default=False)
    is_message_blocked = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(default=datetime.now)

    class Meta:
        table = "users"