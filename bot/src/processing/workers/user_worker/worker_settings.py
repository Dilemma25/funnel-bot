from src.core.logging_config import setup_logging
logger = setup_logging(__name__, service="user_worker")

import asyncio
from datetime import timezone
from datetime import datetime
from datetime import timedelta

from aiogram.exceptions import TelegramBadRequest
from arq.connections import RedisSettings
from arq import Retry
from tortoise.transactions import in_transaction

from src.core.config import settings
from src.controllers.user_states import DayBStates
from src.models import ScheduledTask
from src.models.sent_message import SentMessageTagEnum
from src.processing.tasks.preparable import PreparableTask
from src.safe_bot import SafeBot
from src.core.database import init_db
from src.core.redis import init_redis
from src.processing.task_factory import TaskFactory
from src.views.sent_message import mark_message_as_deleted, track_message
from src.models import UserState
from src.models.offer import OfferCodesEnum


async def startup(ctx):

    logger.info("<< Worker starting up ... >>")

    await init_db()

    ctx["funnel_bot"] = SafeBot(settings.funnel_bot_token)
    ctx["course_sm_bot"] = SafeBot(settings.course_bot_token)
    ctx["task_factory"] = TaskFactory()
    ctx["redis"] = init_redis()

    logger.info("<< Worker initialized! >>")

async def shutdown(ctx):
    from src.core.database import close_db

    logger.info("Worker shutting down...")
    await ctx["funnel_bot"].session.close()
    await ctx["course_sm_bot"].session.close()

    if "redis" in ctx:
        ctx["redis"].close()

    await close_db()

    logger.info("<< Worker shutdown >>")

async def send_scheduled_message(ctx, task_id, task_type, payload):
    """
        Основная функция обработки задачи - заменяет handle_message из consumer

        Args:
            ctx: Контекст от arq (содержит bot, task_factory, redis)
            task_id: ID задачи из БД
            task_type: Тип задачи (send_message, send_document и т.д.)
            payload: Данные для задачи
    """

    logger.info(f"Processing task {task_id}: {task_type}")

    bot: SafeBot = ctx["funnel_bot"]
    task_factory: TaskFactory = ctx["task_factory"]

    job_try = ctx.get("job_try", 1)
    max_tries = ctx.get("max_tries", 3)

    try:

        handler = task_factory.create_task_with_bot(
            task_type=task_type,
            bot=bot,
            payload=payload
        )

        async with in_transaction() as conn:

            task = await ScheduledTask.filter(id=task_id).using_db(conn).first()

            if not task:
                logger.error(f"❌ Task {task_id} not found in database")
                return

            #Если таска не выполнялась
            if not task.processed:
                #Если таска работает с бд
                if isinstance(handler, PreparableTask):

                    await handler.prepare(conn)

                    await task.refresh_from_db(using_db=conn)

                task.processed = True
                await task.save(using_db=conn)

        message = await handler.execute()

        if message and message.message_id:

            await track_message(
                user_id=payload["user_id"],
                telegram_message_id=message.message_id,
                tag=payload["message_tag"],
                stage=payload["message_stage"],
                delete_at=payload["delete_at"],
                delete_on_stage=payload["delete_on_stage"],
            )

        logger.info(f"Task {task_id} completed and saved to DB")

        await asyncio.sleep(0.25)

    except Exception as e:
        logger.error(f"Error handling task {task_id}: {e}", exc_info=True)

        if job_try < max_tries:
            # Delays will be 5s, 10s, 15s
            defer_by = job_try * 5
            print(f"Retrying in {defer_by} seconds...")
            raise Retry(defer=defer_by) from e

        raise Exception("Connection Error: The service is currently unavailable. Please try again later.")

async def delete_message(
                         ctx,
                         message_id,
                         telegram_message_id,
                         chat_id,
                         message_tag,
                     ):
    """Удаление истекших сообщений"""

    logger.info(f"Deleting message {message_id} (tg_msg={telegram_message_id})")

    bot = None

    if message_tag == SentMessageTagEnum.FUNNEL:
        bot = ctx["funnel_bot"]
    if message_tag == SentMessageTagEnum.SM_COURSE:
        bot = ctx["course_sm_bot"]

    try:
        try:
            await bot.delete_message(chat_id=chat_id, message_id=telegram_message_id)
            logger.info(f"✅ Message {telegram_message_id} deleted from Telegram")

        except TelegramBadRequest as e:
            if "message to delete not found" in str(e).lower():
                logger.warning(f"⚠️ Message {telegram_message_id} already deleted")
            else:
                raise

        async with in_transaction() as conn:
            await mark_message_as_deleted(message_id, conn)

        logger.info(f"✅ Message {message_id} marked as deleted")

        await asyncio.sleep(0.25)

    except Exception as e:
        logger.error(f"❌ Error deleting message {message_id}: {e}", exc_info=True)


async def send_nudge(ctx, telegram_user_id: int):
    """
    Отправка напоминания неактивному пользователю

    Args:
        ctx: Контекст ARQ (содержит bot)
        telegram_user_id: Telegram ID пользователя
    """

    logger.info(f"📨 Sending nudge to user {telegram_user_id}")

    bot: SafeBot = ctx["funnel_bot"]

    job_try = ctx.get("job_try", 1)
    max_tries = ctx.get("max_tries", 3)

    try:
        # Получаем текущий стейдж юзера
        user_state = await UserState.filter(
            user_id=telegram_user_id,
            offer__code=OfferCodesEnum.SMART_WALLET
        ).first()

        if not user_state:
            logger.warning(f"⚠️ User {telegram_user_id} not found, skipping nudge")
            return

        # Проверяем что напоминание ещё не отправлялось
        if user_state.nudge_sent:
            logger.info(f"⏭️ Nudge already sent to user {telegram_user_id}, skipping")
            return

        # Текст напоминания
        text = """Слушай, ну мы же не просто так это всё затеяли.

Нам осталось всего одно действие, чтобы пазл сложился.

Ты здесь? Продолжим?"""

        message = await bot.send_message(
            chat_id=telegram_user_id,
            text=text,
            parse_mode="Markdown"
        )

        if message:

            async with in_transaction() as conn:

                user_state.nudge_sent = True
                await user_state.save(using_db=conn)

                await track_message(
                    user_id=telegram_user_id,
                    telegram_message_id=message.message_id,
                    tag=SentMessageTagEnum.FUNNEL,
                    stage='day_a_nudge',
                    delete_at=datetime.now(timezone.utc) + timedelta(hours=6),
                    delete_on_stage=DayBStates.B_1_COLD_SHOWER,
                )

        logger.info(f"✅ Nudge sent to user {telegram_user_id} (stage: {user_state.state})")

        await asyncio.sleep(0.5)

    except TelegramBadRequest as e:
            logger.error(f"❌ Telegram error sending nudge to {telegram_user_id}: {e}")

            if job_try < max_tries:
                defer_by = job_try * 5
                logger.warning(f"🔄 Retrying nudge in {defer_by}s")
                raise Retry(defer=defer_by) from e

    except Exception as e:
        logger.error(f"❌ Error sending nudge to {telegram_user_id}: {e}", exc_info=True)

        if job_try < max_tries:
            defer_by = job_try * 5
            logger.warning(f"🔄 Retrying nudge in {defer_by}s")
            raise Retry(defer=defer_by) from e

        raise Exception(f"Failed to send nudge to {telegram_user_id}: {str(e)}")


class WorkerSettings:
    """Настройки arq worker"""

    redis_settings = RedisSettings(
        host=settings.redis_host,
        port=settings.redis_port,
        database=settings.redis_db
    )


    functions = [
        send_scheduled_message,
        delete_message,
        send_nudge
    ]

    max_jobs = 1

    job_timeout = 60

    keep_result = 3600

    max_tries = 3

    on_startup = startup
    on_shutdown = shutdown

    health_check_interval = 60

    queue_name = "messages_for_users"
