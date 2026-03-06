from aiogram import Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from src.core.redis import init_redis
from src.middlewares.user_check import UserCheckMiddleware
from src.middlewares.error_handler import ErrorHandlerMiddleware
from .setap_routers import setup_routers



def setup_dispatcher() -> Dispatcher:
    """
    Создать и настроить диспетчер

    Returns:
        Настроенный Dispatcher
    """

    # Redis storage для FSM
    redis = init_redis()
    storage = RedisStorage(redis)

    # Создаём диспетчер
    dp = Dispatcher(storage=storage)

    # Подключаем роутеры
    dp.include_router(setup_routers())

    # Подключаем мiddleware
    dp.message.middleware(UserCheckMiddleware())
    dp.update.middleware(ErrorHandlerMiddleware())

    return dp