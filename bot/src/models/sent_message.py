from datetime import timedelta
from src.core.config import settings

from tortoise import fields
from tortoise.models import Model


class SentMessageTagEnum:
    FUNNEL = "funnel"
    COURSE = "course"


class SentMessageDeleteTimings:
    """Таймеры для удаления сообщений"""

    @staticmethod
    def get_default() -> timedelta:
        """12 часов (prod) / 10 минуты (dev)"""
        return timedelta(minutes=10) if settings.is_dev else timedelta(hours=12)

    @staticmethod
    def get_short() -> timedelta:
        """6 часов (prod) / 10 минуты (dev)"""
        return timedelta(minutes=10) if settings.is_dev else timedelta(hours=6)

    @staticmethod
    def get_long() -> timedelta:
        """24 часа (prod) / 10 минуты (dev)"""
        return timedelta(minutes=10) if settings.is_dev else timedelta(hours=24)


class SentMessage(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField(
        model_name="models.User",
        related_name="sent_messages",
        on_delete=fields.CASCADE
    )

    telegram_message_id = fields.BigIntField()

    stage = fields.CharField( # На каком этапе было отправлено
        max_length=100,
        null=True,
    )

    tag = fields.CharField( # Используется для группировки сообщений, например "funnel", "course_smart_wallet"
        max_length=100,
    )

    delete_at = fields.DatetimeField()
    delete_on_stage = fields.CharField(max_length=100)

    is_deleted = fields.BooleanField(default=False)

    class Meta:
        table = "sent_messages"
        indexes = (
            ("user_id", "is_deleted"),  # Поиск активных сообщений юзера
            ("delete_at", "is_deleted"),  # Поиск сообщений для удаления по времени
            ("tag", "is_deleted"),  # Групповое удаление по тегу
        )