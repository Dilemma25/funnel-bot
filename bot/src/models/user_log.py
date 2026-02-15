from tortoise import fields
from tortoise.models import Model
from enum import Enum


class EventTypeEnum(str, Enum):
    """Типы событий для аналитики"""
    STAGE_ENTERED = "stage_entered"  # Вошёл на стейдж
    BUTTON_CLICKED = "button_clicked"  # Нажал кнопку
    USER_DROPPED = "user_dropped"  # Отвалился
    BLOCKED_BOT = "blocked_bot" # заблокировал бота



class UserLog(Model):
    """События для аналитики воронки"""

    id = fields.BigIntField(pk=True)

    # Связь с юзером
    user = fields.ForeignKeyField(
        "models.User",
        related_name="analytics_events",
        on_delete=fields.CASCADE
    )

    offer = fields.ForeignKeyField(
        "models.Offer",
        related_name="analytics_events",
        on_delete=fields.SET_NULL,
        null=True
    )

    event_type = fields.CharEnumField(EventTypeEnum)

    stage = fields.CharField(max_length=100)

    payload = fields.JSONField(default=dict, null=True)

    # Время события
    created_at = fields.DatetimeField(auto_now_add=True, index=True)

    class Meta:
        table = "logs"
        indexes = (
            ("user_id", "event_type"),
            ("event_type", "created_at"),
            ("stage", "created_at"),
        )