from src.core.logging_config import setup_logging

logger = setup_logging(__name__, service="payment_checker_scheduler")

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import timedelta
from datetime import datetime
from tortoise.transactions import in_transaction
import asyncio

from src.models.payment import PaymentStatusEnum
from src.safe_bot import SafeBot
from src.services.payment import PaymentService
from src.services.telgram_notify import TelegramNotifier
from src.views.user_offer_payment import mark_payment, get_pending_payments
from src.views.tasks.cancel_user_tasks import cancel_user_tasks
from src.core.config import settings


class PaymentCheckerScheduler:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()

    async def check_pending_payments(self):
        """Проверяет pending платежи батчами"""
        try:
            threshold = datetime.now() - timedelta(minutes=2)

            pending_payments = await get_pending_payments(
                threshold=threshold,
                limit=20
            )# Батч из 20

            if not pending_payments:
                logger.debug("Нет pending платежей")
                return

            logger.info(f"🔍 Проверка {len(pending_payments)} платежей")

            for payment in pending_payments:
                try:
                    payment_info = await PaymentService.get_payment_info(payment.yookassa_payment_id)

                    logger.info(
                        f"📊 Payment {payment.id}: paid={payment_info.paid}, status={payment_info.status}"
                    )

                    async with in_transaction() as conn:
                        if payment_info.paid and payment_info.status == "succeeded":
                            await mark_payment(
                                payment_id=payment.id,
                                new_status=PaymentStatusEnum.SUCCESSFUL,
                                connection=conn
                            )

                            await payment.fetch_related("user", using_db=conn)

                            user = payment.user

                            bot = SafeBot(settings.funnel_bot_token)

                            await TelegramNotifier.notify_user_succeeded_payment(
                                bot=bot,
                                user_id=user.telegram_id,
                                amount=float(payment_info.amount.value),
                                user_email=user.email,
                            )
                            logger.info(f"✅ Платёж {payment.id} успешен")

                            await asyncio.sleep(0.2)

                            course_name = payment_info.description or "Курс 'Метод умного кошелька'"

                            await TelegramNotifier.notify_course_access(
                                bot=bot,
                                user_id=user.telegram_id,
                                course_name=course_name
                            )

                            await cancel_user_tasks(
                                user_id=user.telegram_id,
                            )

                            await bot.session.close()

                        elif payment_info.status in ["canceled", "failed"]:
                            await mark_payment(
                                payment_id=payment.id,
                                new_status=PaymentStatusEnum.FAILED,
                                connection=conn
                            )
                            logger.info(f"❌ Платёж {payment.id} отменён/провален")

                    await asyncio.sleep(0.25)  # 500ms между запросами

                except Exception as e:
                    logger.error(f"Ошибка проверки платежа {payment.id}: {e}")
                    continue

        except Exception as e:
            logger.error(f"Критическая ошибка в check_pending_payments: {e}", exc_info=True)

    def start(self):
        """Запуск scheduler'а"""
        self.scheduler.add_job(
            self.check_pending_payments,
            'interval',
            minutes=1,
            id='payment_checker_scheduler',
            replace_existing=True
        )

        self.scheduler.start()
        logger.info("✅ Payment checker запущен (интервал: 1 минута)")

    def shutdown(self):
        """Остановка scheduler'а"""
        self.scheduler.shutdown()
        logger.info("⏹ Payment checker остановлен")