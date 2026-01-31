from tortoise import fields
from tortoise.models import Model


class ScheduledTask(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField(
        "models.User",
        on_delete=fields.CASCADE,
        null=True,
    )
    payload = fields.JSONField()
    type = fields.CharField(max_length=50)
    run_at = fields.DatetimeField()
    processed = fields.BooleanField(default=False)

    class Meta:
        table = "scheduled_tasks"