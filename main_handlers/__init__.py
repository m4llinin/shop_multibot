__all__ = ['register_main_handler']

import asyncio

from aiogram import Router, F
from aiogram.filters import Command

from utils import load_texts
from .user_panel import register_handlers_user_panel
from .admin_panel import register_handlers_admin_panel

from .start import start
from .information import information
from .constructor import constructor, constructor_clb

texts: dict = asyncio.run(load_texts())


def register_main_handler(router: Router):
    router.message.register(start, Command("start"))
    router.message.register(information, F.text == texts['information'])
    router.message.register(constructor, F.text == texts['my_shops'])
    router.callback_query.register(constructor_clb, F.data == "constructor")

    register_handlers_user_panel(router)
    register_handlers_admin_panel(router)
