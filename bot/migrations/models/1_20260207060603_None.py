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
CREATE TABLE IF NOT EXISTS "userofferpayment" (
    "id" VARCHAR(200) NOT NULL PRIMARY KEY,
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
    "mffXp5/R/pn68p"
)
