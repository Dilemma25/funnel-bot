import asyncio
import logging

from src.core import init_redis
from src.core.database import init_db
from src.core.database import close_db
from src.processing.consumers.user_message_consumer import UserMessageConsumer
from src.safe_bot import SafeBot
from src.core.config import config
from src.processing.task_factory import TaskFactory


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():

    try:
        await init_db()

        redis = init_redis()
        bot = SafeBot(config["BOT_TOKEN"])
        task_factory = TaskFactory()
        stream_key = config["REDIS_STREAM_KEY"]

        consumer = UserMessageConsumer(
            bot=bot,
            stream_key=stream_key,
            consumer_group="test_group",
            consumer_name="test_consumer",
            task_factory=task_factory,
            redis=redis,
        )

        logger.info("Consumer инициализирован")

        await consumer.process_messages()

    except Exception as e:
        logger.error(f"Ошибка в Consumer:{e}", exc_info=True)

    finally:
        logger.info("Consumer: завершил работу")
        await close_db()

if __name__ == "__main__":
    asyncio.run(main())