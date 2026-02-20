from src.core.logging_config import setup_logging

logger = setup_logging(__name__, service="webhook_yookassa")

from src.services.payment import PaymentService

from tortoise.transactions import in_transaction
from yookassa.domain.notification import WebhookNotificationFactory
from yookassa.domain.notification import WebhookNotificationEventType

from src.models.payment import PaymentStatusEnum

from src.core.config import settings
from src.core.database import init_db
from src.core.database import close_db
from src.safe_bot import SafeBot
from src.views.user_offer_payment import mark_payment_by_yookassa_id
from src.services.telgram_notify import TelegramNotifier

from fastapi import Request
from fastapi import HTTPException
from fastapi import FastAPI
from fastapi import Response

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    logger.info("🚀 Starting webhook server...")

    # === STARTUP ===
    try:
        # Инициализация БД
        try:
            await init_db()

        except Exception as e:
            logger.error(f"Database connection error : {e}", exc_info=True)

        logger.info("✅ Database initialized")

        # Создание бота
        bot = SafeBot(settings.funnel_bot_token)
        fastapi_app.state.bot = bot
        logger.info("✅ Bot initialized")

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        raise

    yield  # Сервер работает

    # === SHUTDOWN ===
    try:
        logger.info("🛑 Shutting down webhook server...")

        bot: SafeBot = fastapi_app.state.bot

        if bot:
            # Закрытие сессии бота
            await bot.session.close()
            logger.info("✅ Bot session closed")

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)

    finally:
        await close_db()
        logger.info("✅ Database closed")

app = FastAPI(
    title="YOOKASSA Webhook Server",
    description="Веб хук для юкасы",
    version="1.0.0",
    lifespan=lifespan,
)

def get_real_ip(request: Request) -> str:
    x_forwarded_for = request.headers.get("x-forwarded-for")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.client.host

@app.post("/webhooks/yookassa")
async def yookassa_webhook(request: Request):
    try:
        client_ip = get_real_ip(request)

        logger.warning(f"FINAL IP USED FOR CHECK: {client_ip}")

        if not PaymentService.check_ip(client_ip):
            logger.warning(f"⚠️ YooKassa webhook from unknown IP: {client_ip}")
            raise HTTPException(status_code=403, detail="Forbidden")

        # Получаем данные
        data = await request.json()

        logger.info(f"💰 Received YooKassa webhook from {client_ip}: {data.get('event')}")

        some_data = None

        try:
            notification_object = WebhookNotificationFactory().create(data)

            response_object = notification_object.object
            event = notification_object.event

        except Exception as e:
            logger.error(f"⚠️ Invalid YooKassa notification: {e}")
            raise HTTPException(status_code=400, detail="Invalid notification")

        if event in (
                WebhookNotificationEventType.PAYMENT_SUCCEEDED,
                WebhookNotificationEventType.PAYMENT_CANCELED,
        ):
            some_data = {
                "payment_id" : response_object.id,
            }

        payment_info = await PaymentService.get_payment_info(payment_id=some_data["payment_id"])

        logger.info(f"Yookassa payment status: {payment_info.status}")

        if payment_info:
            payment_status = payment_info.status

            async with in_transaction() as conn:

                if payment_status == "succeeded":

                    # Отмечаем платёж как успешный
                    payment = await mark_payment_by_yookassa_id(
                        yookassa_payment_id=payment_info.id,
                        new_status=PaymentStatusEnum.SUCCESSFUL,
                        connection=conn
                    )

                    logger.info(f"✅ Payment {payment_info.id} marked as successful in DB")

                    # Уведомляем юзера
                    bot: SafeBot = request.app.state.bot

                    await payment.fetch_related("user", using_db=conn)

                    user = payment.user

                    await TelegramNotifier.notify_user_succeeded_payment(
                        bot=bot,
                        user_id=user.telegram_id,
                        amount=payment.amount,
                    )

                elif payment_status == "canceled":
                    # Отмечаем платёж как отменённый
                    await mark_payment_by_yookassa_id(
                        yookassa_payment_id=some_data['payment_id'],
                        new_status=PaymentStatusEnum.CANCELED,
                        connection=conn
                    )

                    logger.info(f"❌ Payment {some_data['payment_id']} marked as canceled in DB")

        return Response(status_code=200)

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"💥 Error processing YooKassa webhook: {e}", exc_info=True)
        return Response(status_code=500)