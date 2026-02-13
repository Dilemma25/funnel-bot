from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import timedelta
from datetime import datetime
import asyncio

from src.models import UserOfferPayment
from src.models.payment import PaymentStatusEnum
from src.services.payment import PaymentService
from src.views.user_offer_payment import mark_payment
from tortoise.transactions import in_transaction
from src.core.logging_config import setup_logging
from src.core.config import settings

logger = setup_logging(__name__, service="payment_checker_scheduler")


class PaymentCheckerScheduler:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()

    async def check_pending_payments(self):
        """Проверяет pending платежи батчами"""
        try:
            threshold = datetime.now() - timedelta(minutes=2)

            pending_payments = await UserOfferPayment.filter(
                status=PaymentStatusEnum.PENDING,
                created_at__lte=threshold
            ).limit(20).all()  # Батч из 20

            if not pending_payments:
                logger.debug("Нет pending платежей")
                return

            logger.info(f"🔍 Проверка {len(pending_payments)} платежей")

            for payment in pending_payments:
                try:
                    status = await PaymentService.check_payment_status(payment.yookassa_payment_id)

                    logger.info(
                        f"📊 Payment {payment.id}: paid={status['paid']}, status={status['status']}"
                    )

                    async with in_transaction() as conn:
                        if status["paid"]:
                            await mark_payment(
                                payment_id=payment.id,
                                new_status=PaymentStatusEnum.SUCCESSFUL,
                                connection=conn
                            )
                            logger.info(f"✅ Платёж {payment.id} успешен")

                        elif (
                                status["status"] in ["canceled", "failed"]
                                # or (payment.created_at and #TODO время жизни платежа перенести в конфиг или другое место
                                #                            #TODO подумать насчет валидности самостоятельного закрытия платежа
                                #     (datetime.now(settings.timezone) - payment.created_at).total_seconds() > 100)
                        ):
                            await mark_payment(
                                payment_id=payment.id,
                                new_status=PaymentStatusEnum.FAILED,
                                connection=conn
                            )
                            logger.info(f"❌ Платёж {payment.id} отменён/провален")

                    await asyncio.sleep(0.5)  # 500ms между запросами

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