__all__ = ['register_handlers_user_panel']

from aiogram import Router, F

from .add_new_shop import add_new_shop, new_shop

from states.main_bot import AddShop


def register_handlers_user_panel(router: Router):
    router.callback_query.register(add_new_shop, F.data == "create_shop")
    router.message.register(new_shop, F.text, AddShop.token)
