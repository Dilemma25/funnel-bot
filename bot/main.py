import asyncio

from src.core.config import settings
from src.core.logging_config import setup_logging

logger = setup_logging(__name__, service=settings.service_name)

from src.bootstrap.course_bot.bootstrap import start_app as start_course_bot
from src.bootstrap.funnel_bot.bootstrap import start_app as start_funnel_bot



def main():
    service_name = settings.service_name

    if not service_name:
        raise ValueError("SERVICE_NAME environment variable is required")

    service_name = service_name.lower()

    if service_name == "funnel_bot":
        logger.info("🚀 Starting funnel bot...")
        asyncio.run(start_funnel_bot())

    elif service_name == "course_bot":

        logger.info("🚀 Starting course bot...")
        asyncio.run(start_course_bot())

    else:
        raise ValueError(f"Unknown SERVICE_NAME: {service_name}")


if __name__ == "__main__":
    main()