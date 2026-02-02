from aiogram import Router

admin_router = Router()

from .append_file import add_file_command
from .start import start