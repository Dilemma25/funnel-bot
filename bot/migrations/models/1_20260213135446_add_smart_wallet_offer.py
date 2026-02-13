from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        INSERT INTO offers (id, code, title, description, base_price) VALUES
            (1, 'SMART_WALLET', 'Метод умного кошелька', 'Курс про правильное распоряжение деньгами', 3990.0)
            ON CONFLICT (id) DO NOTHING;
        
        SELECT setval('offers_id_seq', (SELECT MAX(id) FROM offers));
        """


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "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"
)
