from aiogram import Router
from src.controllers.smart_wallet_course.handlers import smart_wallet_router
from src.controllers.admin.handlers import admin_router


def setup_routers():

    main_router = Router()

    main_router.include_router(smart_wallet_router)
    main_router.include_router(admin_router)

    return main_router