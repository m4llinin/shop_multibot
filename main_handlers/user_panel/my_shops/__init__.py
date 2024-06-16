__all__ = ['shops_router']

from aiogram import Router, F

from states.main_bot import AddUsersDB, LinkChannel, EditToken

from .my_shops import my_shops, my_shops_list, shop_profile
from .on_off import on_off
from .statistics import statistics
from .settings.main_menu import main_menu_settings
from .settings.on_off_notification import on_off_notification
from .settings.users_db import users_db, get_users_db, send_users_db
from .settings.extra_charge import extra_charge, percent
from .settings.link_channel import link_channel, linked_channel
from .settings.edit_token import edit_token, get_edit_token
from .settings.delete_shop import delete_shop

shops_router = Router()

shops_router.callback_query.register(my_shops, F.data == "my_shops")
shops_router.callback_query.register(my_shops_list, F.data == "get_shops_list")
shops_router.callback_query.register(shop_profile, lambda x: x.data.startswith("shop_"))

shops_router.callback_query.register(on_off, lambda x: x.data.startswith("on_") or x.data.startswith("off_"))

shops_router.callback_query.register(statistics, lambda x: x.data.startswith("statistics_"))

shops_router.callback_query.register(main_menu_settings, lambda x: x.data.startswith("settings_"))
shops_router.callback_query.register(on_off_notification, lambda x: x.data.startswith("notification_"))

shops_router.callback_query.register(users_db, lambda x: x.data.startswith("users_"))
shops_router.message.register(get_users_db, F.document, AddUsersDB.db)
shops_router.callback_query.register(send_users_db, lambda x: x.data.startswith("get_users_"))

shops_router.callback_query.register(extra_charge, lambda x: x.data.startswith("extra_charge_"))
shops_router.callback_query.register(percent, lambda x: x.data.startswith("percent_"))

shops_router.callback_query.register(link_channel, lambda x: x.data.startswith("link_"))
shops_router.message.register(linked_channel, LinkChannel.channel)

shops_router.callback_query.register(edit_token, lambda x: x.data.startswith("change_token_"))
shops_router.message.register(get_edit_token, F.text, EditToken.token)

shops_router.callback_query.register(delete_shop, lambda x: x.data.startswith("delete_shop_"))
