from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
    SELECT 1;
       """


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
    SELECT 1;
        """


MODELS_STATE = (
    "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"
    "y/8BKxQ2cw=="
)
