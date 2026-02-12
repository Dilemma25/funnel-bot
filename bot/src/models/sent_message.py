from tortoise import fields
from tortoise.models import Model


class SentMessageTagEnum:
    FUNNEL = "funnel"
    COURSE = "course"


class SentMessage(Model):
    id = fields.IntField(pk=True)
    user_id = fields.ForeignKeyField(
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