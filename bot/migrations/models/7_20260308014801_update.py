from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "media" ALTER COLUMN "bot_tag" SET NOT NULL;
        ALTER TABLE "media" ALTER COLUMN "file_type" SET NOT NULL;   
           """


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "media" ALTER COLUMN "bot_tag" DROP NOT NULL;
        ALTER TABLE "media" ALTER COLUMN "file_type" DROP NOT NULL;   
           """


MODELS_STATE = (
    "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"
    "8D+1iOsc//m0BJc55Pby9B97MKVY"
)
