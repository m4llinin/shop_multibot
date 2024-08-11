__all__ = ['register_main_handler']

import asyncio

from aiogram import Router, F
from aiogram.filters import Command

from shop_handlers import privacy
from states.main_bot import SupportSolution

from utils import load_texts
from .user_panel import register_handlers_user_panel
from .admin_panel import register_handlers_admin_panel

from .start import start, start_clb
from .information import information, information_clb, faq, privacy_policy
from .constructor import constructor, constructor_clb
from .support_solution import successful_support, bad_support, get_solution
from .loyalty_level import successful_level, bad_level

texts: dict = asyncio.run(load_texts())


def register_main_handler(router: Router):
    router.message.register(privacy, Command("privacy"))

    router.message.register(start, Command("start"))
    router.callback_query.register(start_clb, F.data == "start")

    router.message.register(information, F.text == texts['information'])
    router.callback_query.register(information_clb, F.data == "information")
    router.callback_query.register(faq, F.data == "faq")
    router.callback_query.register(privacy_policy, F.data == "privacy_policy")

    router.message.register(constructor, F.text == texts['my_shops'])
    router.callback_query.register(constructor_clb, F.data == "constructor")

    router.callback_query.register(successful_support, lambda x: x.data.startswith("successful_support_"))
    router.message.register(get_solution, F.text, SupportSolution.text)
    router.callback_query.register(bad_support, lambda x: x.data.startswith("bad_support_"))

    router.callback_query.register(successful_level, lambda x: x.data.startswith("suc_level_"))
    router.callback_query.register(bad_level, F.data == "bad_level")

    register_handlers_user_panel(router)
    register_handlers_admin_panel(router)
