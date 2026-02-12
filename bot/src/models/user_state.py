from tortoise.models import Model
from tortoise import fields


class UserState(Model):
    user_id = fields.BigIntField(pk=True)
    state = fields.CharField(max_length=255, null=True)
    data = fields.JSONField(default=dict)

    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "user_states"