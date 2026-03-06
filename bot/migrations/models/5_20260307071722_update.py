from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" ADD "email" VARCHAR(200);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" DROP COLUMN "email";"""


MODELS_STATE = (
    "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"
    "=="
)
