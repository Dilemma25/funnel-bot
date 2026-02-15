from tortoise.models import Model
from tortoise import fields
from datetime import datetime

from src.core.config import settings

class UserState(Model):
    id = fields.IntField(pk=True)  # ← Отдельный PK

    user = fields.ForeignKeyField(
        "models.User",
        related_name="states",
        on_delete=fields.CASCADE
    )

    offer = fields.ForeignKeyField(
        "models.Offer",
        related_name="user_states",
        on_delete=fields.CASCADE
    )

    state = fields.CharField(max_length=100, null=True)
    last_activity_at = fields.DatetimeField(default=lambda: datetime.now(settings.timezone))

    #Отправлялось ли напоминание
    nudge_sent = fields.BooleanField(default=False)

    class Meta:
        table = "user_states"
        unique_together = ("user", "offer")