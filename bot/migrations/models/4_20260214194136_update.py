from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "sent_messages" DROP CONSTRAINT IF EXISTS "fk_sent_mes_users_60bef6b6";
        ALTER TABLE "sent_messages" RENAME COLUMN "user_id_id" TO "user_id";
        ALTER TABLE "user_states" ALTER COLUMN "last_activity_at" SET DEFAULT '2026-02-14 09:41:32.581961+00:00';
        ALTER TABLE "sent_messages" ADD CONSTRAINT "fk_sent_mes_users_a742b69d" FOREIGN KEY ("user_id") REFERENCES "users" ("telegram_id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "sent_messages" DROP CONSTRAINT IF EXISTS "fk_sent_mes_users_a742b69d";
        ALTER TABLE "user_states" ALTER COLUMN "last_activity_at" SET DEFAULT '2026-02-13 03:59:19.347161+00:00';
        ALTER TABLE "sent_messages" RENAME COLUMN "user_id" TO "user_id_id";
        ALTER TABLE "sent_messages" ADD CONSTRAINT "fk_sent_mes_users_60bef6b6" FOREIGN KEY ("user_id_id") REFERENCES "users" ("telegram_id") ON DELETE CASCADE;"""


MODELS_STATE = (
    "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"
    "SldU74nbw1XqDZfnh5+gOJr3mj"
)
