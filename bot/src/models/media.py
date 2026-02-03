from tortoise.models import Model
from tortoise import fields


class Media(Model):
    name = fields.CharField(max_length=200)
    file_id = fields.CharField(max_length=500)

    class Meta:
        table_name = "media"