from tortoise import BaseDBAsyncClient
from src.core.config import settings

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    admin_id = settings.admin_ids[0]

    return f"""
        -- Вставляем админа только если его еще нет
        INSERT INTO users (telegram_id, role)
        VALUES ({admin_id}, 'admin')
        ON CONFLICT (telegram_id) DO NOTHING;
    """
    #  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    #  Если уже есть - ничего не делаем


async def downgrade(db: BaseDBAsyncClient) -> str:
    admin_id = settings.admin_ids[0]

    return f"""
        -- Удаляем админа при откате миграции
        DELETE FROM users
        WHERE telegram_id = {admin_id}
          AND role = 'admin';
    """


MODELS_STATE = (
    "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"
)
