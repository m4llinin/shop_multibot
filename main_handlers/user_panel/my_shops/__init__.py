__all__ = ['shops_router']

from aiogram import Router, F

from states.main_bot import AddUsersDB, LinkChannel, EditToken, AddMail

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

from .mailing import (mailing_list, add_mail, get_text_photo, view_adding_mail, add_date, get_date, add_btn, get_btn,
                      save_mail, change_page, view_profile_mail, view_mail, delete_mail, just_page, edit_mail_text,
                      edit_mail_photo, get_edit_mail_text, get_edit_mail_photo)

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

shops_router.callback_query.register(mailing_list, lambda x: x.data.startswith("mailing_"))
shops_router.callback_query.register(add_mail, F.data == "add_mail")
shops_router.message.register(get_text_photo, F.text, AddMail.text)
shops_router.message.register(get_text_photo, F.photo, AddMail.text)
shops_router.callback_query.register(view_adding_mail, F.data == "view_adding_mail")
shops_router.callback_query.register(add_date, F.data == "date")
shops_router.message.register(get_date, F.text, AddMail.date)
shops_router.callback_query.register(add_btn, F.data == "add_btn")
shops_router.message.register(get_btn, F.text, AddMail.button)
shops_router.callback_query.register(save_mail, F.data == "save_btn")

shops_router.callback_query.register(change_page, lambda x: x.data == "back_page_mail" or x.data == "next_page_mail")
shops_router.callback_query.register(view_profile_mail, lambda x: x.data.startswith("mail_"))
shops_router.callback_query.register(view_mail, F.data == "view_mail")
shops_router.callback_query.register(delete_mail, F.data == "delete_mail")

shops_router.callback_query.register(edit_mail_photo, F.data == f"edit_mail_photo")
shops_router.callback_query.register(edit_mail_text, F.data == f"edit_mail_text")
shops_router.message.register(get_edit_mail_text, F.text, AddMail.edit_text)
shops_router.message.register(get_edit_mail_photo, F.photo, AddMail.edit_photo)

shops_router.callback_query.register(just_page, F.data == "just_page")
