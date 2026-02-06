from tortoise.models import Model
from tortoise import fields


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

    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "media"
        unique_together = ("offer", "code")