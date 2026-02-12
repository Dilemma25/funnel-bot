import asyncio
from src.core.database import init_db
from src.core.database import close_db
from src.core.logging_config import setup_logging
from src.processing.schedulers.payment_checker_scheduler.payment_checker_scheduler import PaymentCheckerScheduler
from tortoise import run_async

logger = setup_logging(__name__, service="payment_checker_scheduler")


async def main():
    run_async(init_db())
    logger.info("PaymentCheckerScheduler: инициализирован")

    checker = PaymentCheckerScheduler()
    checker.start()
    logger.info("PaymentCheckerScheduler: запущен")

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        logger.info("Получен сигнал завершения...")
        checker.shutdown()
        await close_db()
        logger.info("PaymentCheckerScheduler: завершён")


if __name__ == "__main__":
    asyncio.run(main())