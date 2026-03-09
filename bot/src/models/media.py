from enum import Enum

from tortoise.models import Model
from tortoise import fields


class BotTagEnum(str, Enum):
    FUNNEL = "funnel_bot"
    SMART_WALLET_COURSE = "smart_wallet_course_bot"

class MediaFileTypeEnum(str, Enum):
    VIDEO = "video"
    DOCUMENT = "document"
    PHOTO = "photo"
    VIDEO_NOTE = "video_note"
    AUDIO = "audio"
    ANIMATION  = "animation"


class Media(Model):
    id = fields.IntField(pk=True)

    offer = fields.ForeignKeyField(
        "models.Offer",
        related_name="media_files",
        on_delete=fields.SET_NULL,
        null=True,
    )

    code = fields.CharField(max_length=200)
    file_id = fields.CharField(max_length=500)

    file_type = fields.CharEnumField(
        MediaFileTypeEnum,
    )

    bot_tag = fields.CharEnumField(BotTagEnum)

    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "media"
        unique_together = ("offer", "code")