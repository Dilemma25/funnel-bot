from aiogram import Router
from src.controllers.funnel_bot.admin.handlers import admin_router
from src.controllers.funnel_bot.day_a.handlers import day_a_router
from src.controllers.echo import echo_router
from src.controllers.support.handlers import support_router


def setup_routers():

    main_router = Router()
    main_router.include_router(admin_router)
    main_router.include_router(support_router)

    main_router.include_router(day_a_router)
    main_router.include_router(echo_router)

    return main_router