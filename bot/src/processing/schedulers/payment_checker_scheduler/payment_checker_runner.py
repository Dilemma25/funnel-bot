import asyncio

from src.core.logging_config import setup_logging
logger = setup_logging(__name__, service="payment_checker_scheduler")

from src.core.database import init_db, close_db
from src.processing.schedulers.payment_checker_scheduler.payment_checker_scheduler import PaymentCheckerScheduler

# TODO добавить лок на редис
async def main():
    logger.info("Payment checker: starting")
    is_db_init = False

    try:
        await init_db()
        is_db_init = True

        scheduler = PaymentCheckerScheduler()
        await scheduler.check_pending_payments()

    except Exception as e:
        logger.error(f"Error in payment checker: {e}", exc_info=True)

    finally:
        logger.info("Payment checker: completed")
        if is_db_init:
            await close_db()


if __name__ == "__main__":
    asyncio.run(main())