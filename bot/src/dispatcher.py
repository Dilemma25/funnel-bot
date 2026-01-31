from aiogram import Dispatcher
from src.controllers.handlers.start import start_router
from src.controllers.handlers.echo import echo_router
from src.middlewares.user_check import UserCheckMiddleware

dispatcher = Dispatcher()

dispatcher.include_routers(
    start_router,
    echo_router,
)
dispatcher.message.middleware(UserCheckMiddleware())
