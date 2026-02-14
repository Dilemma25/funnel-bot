import asyncio

from src.core.logging_config import setup_logging
setup_logging(__name__, service="bot")

from src.bootstrap import start_app



if __name__ == "__main__":
    asyncio.run(start_app())