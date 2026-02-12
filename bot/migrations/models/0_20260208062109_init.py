from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "offers" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "code" VARCHAR(50) NOT NULL UNIQUE,
    "title" VARCHAR(255) NOT NULL,
    "description" TEXT,
    "base_price" DOUBLE PRECISION NOT NULL
);
CREATE TABLE IF NOT EXISTS "media" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "code" VARCHAR(200) NOT NULL,
    "file_id" VARCHAR(500) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "offer_id" INT REFERENCES "offers" ("id") ON DELETE SET NULL,
    CONSTRAINT "uid_media_offer_i_5a4c0f" UNIQUE ("offer_id", "code")
);
CREATE TABLE IF NOT EXISTS "users" (
    "telegram_id" BIGSERIAL NOT NULL PRIMARY KEY,
    "is_message_blocked" BOOL NOT NULL DEFAULT False,
    "created_at" TIMESTAMPTZ NOT NULL
);
CREATE TABLE IF NOT EXISTS "scheduled_tasks" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "payload" JSONB NOT NULL,
    "type" VARCHAR(50) NOT NULL,
    "run_at" TIMESTAMPTZ NOT NULL,
    "processed" BOOL NOT NULL DEFAULT False,
    "user_id" BIGINT REFERENCES "users" ("telegram_id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "user_offers" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "discount_price" DOUBLE PRECISION,
    "discount_expires_at" TIMESTAMPTZ,
    "created_at" TIMESTAMPTZ NOT NULL,
    "offer_id" INT NOT NULL REFERENCES "offers" ("id") ON DELETE CASCADE,
    "user_id" BIGINT NOT NULL REFERENCES "users" ("telegram_id") ON DELETE CASCADE,
    CONSTRAINT "uid_user_offers_user_id_ca447f" UNIQUE ("user_id", "offer_id")
);
CREATE TABLE IF NOT EXISTS "user_offer_payments" (
    "id" SERIAL PRIMARY KEY,
    "yookassa_payment_id" VARCHAR(200) NOT NULL,
    "amount" DOUBLE PRECISION NOT NULL,
    "status" VARCHAR(30) NOT NULL DEFAULT 'PENDING',
    "created_at" TIMESTAMPTZ NOT NULL,
    "user_offer_id" INT REFERENCES "user_offers" ("id") ON DELETE SET NULL
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "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"
    "mnl9f/AZBKsFo="
)
