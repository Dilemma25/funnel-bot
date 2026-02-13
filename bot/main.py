import asyncio

from src.bootstrap import start_app
from src.core.logging_config import setup_logging


if __name__ == "__main__":
    setup_logging(__name__, service="bot")
    asyncio.run(start_app())