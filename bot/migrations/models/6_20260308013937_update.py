from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
    -- Добавляем колонку bot_tag
    ALTER TABLE "media"
        ADD COLUMN "bot_tag" VARCHAR(23) DEFAULT 'funnel_bot';

    -- Обновляем bot_tag для smart_wallet_course_bot
    UPDATE media
    SET bot_tag = 'smart_wallet_course_bot'
    WHERE id IN (14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27);

    -- Убеждаемся что все строки заполнены
    UPDATE media
    SET bot_tag = 'funnel_bot'
    WHERE bot_tag IS NULL;
        
    COMMENT ON COLUMN "media"."bot_tag" IS 'FUNNEL: funnel_bot\nSMART_WALLET_COURSE: smart_wallet_course_bot';

    -- Добавляем колонку file_type
    ALTER TABLE "media"
        ADD COLUMN "file_type" VARCHAR(10);
    COMMENT ON COLUMN "media"."file_type" IS 'VIDEO: video\nDOCUMENT: document\nPHOTO: photo\nVIDEO_NOTE: video_note\nAUDIO: audio\nANIMATION: animation';

    -- Проставляем file_type по префиксу file_id
    UPDATE media
    SET file_type = 'video'
    WHERE file_id LIKE 'BAA%';

    UPDATE media
    SET file_type = 'document'
    WHERE file_id LIKE 'BQA%';

    UPDATE media
    SET file_type = 'photo'
    WHERE file_id LIKE 'AgA%';

    UPDATE media
    SET file_type = 'video_note'
    WHERE file_id LIKE 'DQA%';
    """

async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "media" 
        DROP COLUMN "bot_tag",
        DROP COLUMN "file_type";
           """


MODELS_STATE = (
    "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"
    "Q2sRE/6nFnGd4z+fluAyx9xeXv4DSUqlDQ=="
)
