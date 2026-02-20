from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "sent_messages" DROP CONSTRAINT IF EXISTS "fk_sent_mes_users_60bef6b6";
        CREATE TABLE IF NOT EXISTS "user_history" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "event_type" VARCHAR(14) NOT NULL,
    "stage" VARCHAR(100) NOT NULL,
    "payload" JSONB,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "offer_id" INT REFERENCES "offers" ("id") ON DELETE SET NULL,
    "user_id" BIGINT NOT NULL REFERENCES "users" ("telegram_id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_user_histor_created_1696cb" ON "user_history" ("created_at");
CREATE INDEX IF NOT EXISTS "idx_user_histor_user_id_0df9c1" ON "user_history" ("user_id", "event_type");
CREATE INDEX IF NOT EXISTS "idx_user_histor_event_t_97c1f6" ON "user_history" ("event_type", "created_at");
CREATE INDEX IF NOT EXISTS "idx_user_histor_stage_5ad5ba" ON "user_history" ("stage", "created_at");
COMMENT ON COLUMN "user_history"."event_type" IS 'STAGE_ENTERED: stage_entered\nBUTTON_CLICKED: button_clicked\nUSER_DROPPED: user_dropped\nBLOCKED_BOT: blocked_bot';
COMMENT ON TABLE "user_history" IS 'События для аналитики воронки';
        ALTER TABLE "sent_messages" RENAME COLUMN "user_id_id" TO "user_id";
        ALTER TABLE "user_offers" ADD "status" VARCHAR(14) NOT NULL DEFAULT 'active';
        COMMENT ON COLUMN "user_offers"."status" IS 'ACTIVE: active\nPURCHASED: purchased\nDROPPED: dropped\nBLOCKED_BOT: blocked_bot\nCOMPLETED_FREE: completed_free';
        ALTER TABLE "sent_messages" ADD CONSTRAINT "fk_sent_mes_users_a742b69d" FOREIGN KEY ("user_id") REFERENCES "users" ("telegram_id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "sent_messages" DROP CONSTRAINT IF EXISTS "fk_sent_mes_users_a742b69d";
        ALTER TABLE "user_offers" DROP COLUMN "status";
        ALTER TABLE "sent_messages" RENAME COLUMN "user_id" TO "user_id_id";
        DROP TABLE IF EXISTS "user_history";
        ALTER TABLE "sent_messages" ADD CONSTRAINT "fk_sent_mes_users_60bef6b6" FOREIGN KEY ("user_id_id") REFERENCES "users" ("telegram_id") ON DELETE CASCADE;"""


MODELS_STATE = (
    "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"
)
