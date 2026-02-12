from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "user_states" (
    "user_id" BIGSERIAL NOT NULL PRIMARY KEY,
    "state" VARCHAR(255),
    "data" JSONB NOT NULL,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "user_states";"""


MODELS_STATE = (
    "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"
)
