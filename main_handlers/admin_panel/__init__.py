__all__ = ['register_handlers_admin_panel']

import asyncio

from aiogram import Router, F

from utils import load_texts
from states.main_bot import AddCategory, AddSubcategory, AddGoods, EditCount, LinkChannelAdmin, ChangeStatus, \
    AddAdminMail

from .admin import admin_panel, admin_panel_clb

from .view_category import view_category, view_subcategory, view_good_list, view_good
from .add_category import add_category, get_name_category, get_description_category
from .add_subcategory import add_subcategory, insert_subcategory, get_name_subcategory, get_description_subcategory
from .add_good import (add_good, insert_good, insert_subcat, get_good_name, get_good_description, get_good_price,
                       get_good_count, get_product)

from .delete import delete_good, delete_subcategory, delete_category
from .edit_good import edit_good_count, get_count

from .link_channel import link_channel, linked_channel
from .change_status import change_status, get_status, get_username

from .statistics import statistics_router

from .mailing import (admin_add_btn, admin_get_btn, admin_add_mail, admin_mailing_list, admin_add_date, admin_get_date,
                      admin_view_adding_mail, admin_change_page, admin_get_text_photo, admin_save_mail, admin_view_mail,
                      admin_view_profile_mail, admin_delete_mail)

texts: dict = asyncio.run(load_texts())


def register_handlers_admin_panel(router: Router):
    router.message.register(admin_panel, F.text == texts['admin_panel_btn'])
    router.callback_query.register(admin_panel_clb, F.data == "admin_panel")

    router.callback_query.register(view_category, F.data == "view_category")
    router.callback_query.register(view_subcategory, lambda x: x.data.startswith("category_"))
    router.callback_query.register(view_good_list, lambda x: x.data.startswith("subcategory_"))
    router.callback_query.register(view_good, lambda x: x.data.startswith("good_"))

    router.callback_query.register(add_category, F.data == "add_category")
    router.message.register(get_name_category, F.text, AddCategory.name)
    router.message.register(get_description_category, F.text, AddCategory.description)

    router.callback_query.register(add_subcategory, F.data == "add_subcategory")
    router.callback_query.register(insert_subcategory, lambda x: x.data.startswith("insert_subcategory_"))
    router.message.register(get_name_subcategory, F.text, AddSubcategory.name)
    router.message.register(get_description_subcategory, F.text, AddSubcategory.description)

    router.callback_query.register(add_good, F.data == "add_good")
    router.callback_query.register(insert_subcat, lambda x: x.data.startswith("insert_subcat_"))
    router.callback_query.register(insert_good, lambda x: x.data.startswith("insert_good_"))
    router.message.register(get_good_name, F.text, AddGoods.name)
    router.message.register(get_good_description, F.text, AddGoods.description)
    router.message.register(get_good_price, F.text, AddGoods.price)
    router.message.register(get_good_count, F.text, AddGoods.count)
    router.message.register(get_product, F.text, AddGoods.product)

    router.callback_query.register(delete_good, lambda x: x.data.startswith("delete_good_"))
    router.callback_query.register(delete_subcategory, lambda x: x.data.startswith("delete_subcategory_"))
    router.callback_query.register(delete_category, lambda x: x.data.startswith("delete_category_"))

    router.callback_query.register(edit_good_count, lambda x: x.data.startswith("edit_good_"))
    router.message.register(get_count, F.text, EditCount.amount)

    router.callback_query.register(link_channel, F.data == "link_channel")
    router.message.register(linked_channel, LinkChannelAdmin.channel)

    router.callback_query.register(change_status, F.data == "change_status")
    router.message.register(get_username, F.text, ChangeStatus.user)
    router.callback_query.register(get_status,
                                   lambda x: x.data in ["main_admin", "admin", "partner", "linker", "super_partner"])

    router.callback_query.register(admin_mailing_list, F.data == "admin_mailing_list")
    router.callback_query.register(admin_change_page,
                                   lambda x: x.data == "back_page_admin_mail" or x.data == "next_page_admin_mail")
    router.callback_query.register(admin_view_adding_mail, F.data == "admin_view_adding_mail")
    router.callback_query.register(admin_add_mail, F.data == "add_admin_mail")
    router.message.register(admin_get_text_photo, F.text, AddAdminMail.text)
    router.message.register(admin_get_text_photo, F.photo, AddAdminMail.text)
    router.callback_query.register(admin_add_date, F.data == "admin_date")
    router.message.register(admin_get_date, F.text, AddAdminMail.date)
    router.callback_query.register(admin_add_btn, F.data == "admin_add_btn")
    router.message.register(admin_get_btn, F.text, AddAdminMail.button)
    router.callback_query.register(admin_save_mail, F.data == "admin_save_btn")
    router.callback_query.register(admin_view_profile_mail, lambda x: x.data.startswith("admin_mail_"))
    router.callback_query.register(admin_view_mail, F.data == "admin_view_mail")
    router.message.register(admin_delete_mail, F.data == "admin_delete_mail")

    router.include_router(statistics_router)
