from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "logs" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "event_type" VARCHAR(14) NOT NULL,
    "stage" VARCHAR(100) NOT NULL,
    "payload" JSONB,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "offer_id" INT REFERENCES "offers" ("id") ON DELETE SET NULL,
    "user_id" BIGINT NOT NULL REFERENCES "users" ("telegram_id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_logs_created_0cf83d" ON "logs" ("created_at");
CREATE INDEX IF NOT EXISTS "idx_logs_user_id_8e61fd" ON "logs" ("user_id", "event_type");
CREATE INDEX IF NOT EXISTS "idx_logs_event_t_d1249a" ON "logs" ("event_type", "created_at");
CREATE INDEX IF NOT EXISTS "idx_logs_stage_46b551" ON "logs" ("stage", "created_at");
COMMENT ON COLUMN "logs"."event_type" IS 'STAGE_ENTERED: stage_entered\nBUTTON_CLICKED: button_clicked\nUSER_DROPPED: user_dropped\nBLOCKED_BOT: blocked_bot';
COMMENT ON TABLE "logs" IS 'События для аналитики воронки';
        ALTER TABLE "user_offers" ADD "status" VARCHAR(14) NOT NULL DEFAULT 'active';
        COMMENT ON COLUMN "user_offers"."status" IS 'ACTIVE: active\nPURCHASED: purchased\nDROPPED: dropped\nBLOCKED_BOT: blocked_bot\nCOMPLETED_FREE: completed_free';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user_offers" DROP COLUMN "status";
        DROP TABLE IF EXISTS "logs";"""


MODELS_STATE = (
    "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"
)
