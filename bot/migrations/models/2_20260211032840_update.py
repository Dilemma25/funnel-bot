from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user_offer_payments" ADD "yookassa_payment_id" VARCHAR(200) NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user_offer_payments" DROP COLUMN "yookassa_payment_id";"""


MODELS_STATE = (
    "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"
    "EoPnNP"
)
