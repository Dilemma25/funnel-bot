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
    "role" VARCHAR(100) NOT NULL DEFAULT 'user',
    "is_message_blocked" BOOL NOT NULL DEFAULT False,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "scheduled_tasks" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "payload" JSONB NOT NULL,
    "type" VARCHAR(50) NOT NULL,
    "run_at" TIMESTAMPTZ NOT NULL,
    "processed" BOOL NOT NULL DEFAULT False,
    "user_id" BIGINT REFERENCES "users" ("telegram_id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "sent_messages" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "telegram_message_id" BIGINT NOT NULL,
    "stage" VARCHAR(100),
    "tag" VARCHAR(100) NOT NULL,
    "delete_at" TIMESTAMPTZ NOT NULL,
    "delete_on_stage" VARCHAR(100) NOT NULL,
    "is_deleted" BOOL NOT NULL DEFAULT False,
    "user_id_id" BIGINT NOT NULL REFERENCES "users" ("telegram_id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_sent_messag_user_id_19a459" ON "sent_messages" ("user_id_id", "is_deleted");
CREATE INDEX IF NOT EXISTS "idx_sent_messag_delete__3da062" ON "sent_messages" ("delete_at", "is_deleted");
CREATE INDEX IF NOT EXISTS "idx_sent_messag_tag_7e9a73" ON "sent_messages" ("tag", "is_deleted");
CREATE TABLE IF NOT EXISTS "user_offers" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "discount_price" DOUBLE PRECISION,
    "discount_expires_at" TIMESTAMPTZ,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "offer_id" INT NOT NULL REFERENCES "offers" ("id") ON DELETE CASCADE,
    "user_id" BIGINT NOT NULL REFERENCES "users" ("telegram_id") ON DELETE CASCADE,
    CONSTRAINT "uid_user_offers_user_id_ca447f" UNIQUE ("user_id", "offer_id")
);
CREATE TABLE IF NOT EXISTS "user_offer_payments" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "yookassa_payment_id" VARCHAR(300) NOT NULL UNIQUE,
    "yookassa_payment_url" VARCHAR(300) NOT NULL,
    "amount" DOUBLE PRECISION NOT NULL,
    "status" VARCHAR(30) NOT NULL DEFAULT 'PENDING',
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "offer_id" INT NOT NULL REFERENCES "offers" ("id") ON DELETE CASCADE,
    "user_id" BIGINT NOT NULL REFERENCES "users" ("telegram_id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "user_states" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "state" VARCHAR(100),
    "last_activity_at" TIMESTAMPTZ NOT NULL DEFAULT '2026-02-13T03:54:00.228809+00:00',
    "nudge_sent" BOOL NOT NULL DEFAULT False,
    "offer_id" INT NOT NULL REFERENCES "offers" ("id") ON DELETE CASCADE,
    "user_id" BIGINT NOT NULL REFERENCES "users" ("telegram_id") ON DELETE CASCADE,
    CONSTRAINT "uid_user_states_user_id_3fbd31" UNIQUE ("user_id", "offer_id")
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
    "eJztXF1zmzgU/SsentLZtOPgOEn7ZidO661jZ2Jnt9NMh5FBJkwweJFo4+nkv6/Et0AQTO"
    "wYUr3Z0r0gHQndc64Ev6WlrUETfbiCmgGkT63fkgWWkPxgKw5bElit4mJagMHc9C0jkznC"
    "DlAxKVwAE0FSpEGkOsYKG7ZFSi3XNGmhrRJDw9LjItcy/nOhgm0d4nvokIq7O8leLMhPUq"
    "uSm0o/fpBfhqXBR4hoPf27elAWBjQ1puWGRn28cgWvV17Z0MKXniG9/VxRbdNdWrHxao3v"
    "bSuyNixMS3VoQQdgSC+PHZf2hzY36HfYRb/psYnfxISPBhfANXGi/yVBUW2LAkpag7wO6v"
    "Qu7+Wj49Pjs87J8Rkx8VoSlZw++d2L++47egiMZ9KTVw8w8C08GGPcPJQzyJ3fA4cPXWif"
    "Ao80OQ1eCFURemFBDF88h7aE3xI8Kia0dHxPQWu3C9D6p3dz/qV3c0Cs3tHe2GRe+7N9HF"
    "TJfh2FNIZwYZhQ4c2/fBQTLs0EslsKyG4BkN0skKoDaZcVgLNYXpAabCxhzqxkPFOQaoHr"
    "h/BHTQEmfdAmlrkOFpECfGfDq8F01ru6pj1ZIvSf6UHUmw1ojeyVrlOlByepoYgu0vp3OP"
    "vSon9b3yfjgYegjbDueHeM7WbfJdom4GJbsexfCtAS611YGgLDDKy3pnMfkdwlOuny/ELN"
    "GcGgXa85gFtYqml8WzxwV+ooMLIIXtoONHTrK1x7QA5Jk4Cl8tboILhPwuvUDsCncBKEpX"
    "ErHPArCvrM3CD9I72C2OvhdDBrjW9HI8nDcQ7Uh1/A0RQGUFpjy3aqJLLNVi3lZboEWED3"
    "EKD9oK1moOUQqgjzfELldQptn1EJAvWWCdTO0UtF/VJBvyDmp0M+NrC5EXyRQzN5k9ztli"
    "Gg3W4+AaV1LIjJlmWgnMHHnIc45VYJ0L0FCS4tGnybMYwoRO3gqvftHcOKRpPx59A8gfL5"
    "aNJPgTsHCCorx1A50/TStEEOuKxbCtsF9avndC2A92Jy2x8NWtc3g/PhdDgZszTTq6RFpM"
    "Dww/HNoDficZr84JwInDS/oFCdhLK49wPny6830AQ5Ezidy6jrTM7QHWb6uYhQnZgbVMfh"
    "llyoLPXb37wrBmMF1ktIHbaDxLV/uQYD4s0OQvjxS58SismUXqdhYOySzU/Ve6i5JtRmAD"
    "1IHFbPGhSyexSaKpjYCprfOJpPlh4StDng/T2djPnoJVxSEN5apHd3mqHiw5ZpIPyj1k8d"
    "DzDa62KqlWZVh2xWiV4gTbU8eDIAF2iBwL6ZUmD7YspxrQq509irmXnThuRJw24XJkpXjq"
    "1ChCBnnenbtgmBlbPUJP1SwzgnjrsauU0DV/mh608mI2bU+sO0WLu96g9uDo7esaIjXMpT"
    "JIkX9/qGnhv6Ek7NSj9/lOVO51Rud07Ousenp92zdhQKs1VFMbE//EyxZDB/NklNYdtCjv"
    "oWNTxFnZg+TIb6vDc9710M9pWgnhK5c0UWCuDNlSyhTVQX01liqCx9y92T2bsknAYK4NQk"
    "YnYn+X+CCJauxEBPFwtmvGVmjAmyugOW4XzYeKnNuUClZXcfrO7V1t1kUCMrqL4RWY4cGp"
    "LnZcnyUanzBkcF5w2OsucNgtWhtNzwzZupNnYCILP2bqI5GEchO/YtO4LhIIOw8bLCcRUP"
    "SMwpYuKRDYlFgo51FIqOq+iqijpBMKoJOy7eu9J2NdplOOSLuxrqOw9bjrALMc9XdLRPe9"
    "yWiDRAZfHQPEX2KoohX7c59mYnb0L71wvvUTap1gE+VK1z01YfqgR6zgVEwBcnw9/syfBK"
    "54FSG+gvPO6Q2bmvXfqj1PGPTBr2BYiwqd/6PQSlABEHpcRBKf6TIs5I7Uxw5L71wDxJxd"
    "JD2dXrD3cRifTfnxEvlO54O0gzkGq7JC5tfmY661rx3HStTqVXPTbNJGhDZODjyiDsq0rK"
    "nX+JLTDiWqFdJwJcKvcupM0bkjb7ful1f9npF8aTPZ/W+pOz+iKlz04gfj4/82RvAbYGqs"
    "w0brmvYtdgI4SRrkXyJCFvy6gUJamu6/MWR9H62Dx9sufNkbVtPwCEQDjWG37fJce9ie98"
    "d0ptm3QKtk062W2TDD6uY74I38C/mUdPdgIxWFK1t5H+jl3+6PeV03lDl5M3LDxnGXi84k"
    "bp9WB8MRx/3tpeaafchCyYj+LbTkLmCpkrZK6QuXWSa0Lmvj2Z629J5ujbaL/yGWEb74+K"
    "7bdGb7+hcMA34avivSBm4TMBwgp5BIyfBl5XYKw8/33xVkluyyfv2/L7o06r3fnUPf7Ubn"
    "+Q5bOz9se/2m3y5wWaoSEsttQ2nOVqOlQQ5EnmwgOcrKM4uPkk1IFQB0Id1AlloQ7+THXQ"
    "g46h3kscaRDUHBbpAhDb1GaPSyiA5xXAT+gg7pdg8zVAwqWZOyg7+awufTQ2ADEwbyaAO9"
    "FR5I6YS6jzv5mXcBHfzEvrnPCbeRu8QLP98PL0P+sLfko="
)
