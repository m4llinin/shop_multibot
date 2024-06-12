__all__ = ['register_shop_handler']

import asyncio

from aiogram import Router, F
from aiogram.filters import Command

from utils import load_texts
from states.shop_bot import UpdateBalance, AddQuery

from .start import start, start_clb
from .catalogue.catalogue import view_category, view_category_clb, view_subcategory, view_good_list, view_good
from .catalogue.good_profile import edit_count_cart, just_count
from .catalogue.buy_good import choose_payment, buy_now_prodamus, buy_now_balance

from .my_profile.my_profile import my_profile, my_profile_clb
from .my_profile.referral_system import referral_system
from .my_profile.my_orders import my_orders_list, order_profile, just_page, edit_page

from .update_balance import update_balance_1, update_balance_2, update_balance_1_message, update_balance_2_message

from .support import (support, support_clb, support_themes, select_theme_support, get_text_query, my_queries,
                      query_profile)

texts: dict = asyncio.run(load_texts())


def register_shop_handler(router: Router):
    router.message.register(start, Command("start"))
    router.callback_query.register(start_clb, F.data == "start")

    router.message.register(view_category, F.text == texts['catalogue'])
    router.message.register(my_profile, F.text == texts['my_profile'])
    router.message.register(update_balance_1_message, F.text == texts['pay_balance_reply'])
    router.message.register(support, F.text == texts['contact'])

    router.callback_query.register(view_subcategory, lambda x: x.data.startswith("category_"))
    router.callback_query.register(view_good_list, lambda x: x.data.startswith("subcategory_"))
    router.callback_query.register(view_good, lambda x: x.data.startswith("good_"))
    router.callback_query.register(view_category_clb, F.data == "view_category")

    router.callback_query.register(edit_count_cart, lambda x: x.data.startswith("plus_") or x.data.startswith("minus_"))
    router.callback_query.register(just_count, F.data == "just_count")

    router.callback_query.register(choose_payment, lambda x: x.data.startswith("buy_good_"))
    router.callback_query.register(buy_now_prodamus, F.data == "pay_card")
    router.callback_query.register(buy_now_balance, F.data == "pay_from_balance")

    router.callback_query.register(my_profile_clb, F.data == "my_profile")
    router.callback_query.register(referral_system, F.data == "referral_sys")

    router.callback_query.register(my_orders_list, F.data == "my_orders")
    router.callback_query.register(order_profile, lambda x: x.data.startswith("my_order_"))
    router.callback_query.register(just_page, F.data == "just_page")
    router.callback_query.register(edit_page, F.data == "back_page")
    router.callback_query.register(edit_page, F.data == "next_page")

    router.callback_query.register(update_balance_1, F.data == "update_balance")
    router.callback_query.register(update_balance_2, lambda x: x.data.startswith("update_balance_"))
    router.message.register(update_balance_2_message, F.text, UpdateBalance.amount)

    router.callback_query.register(support_clb, F.data == "support")
    router.callback_query.register(support_themes, F.data == "add_query")
    router.callback_query.register(select_theme_support, lambda x: x.data.startswith("theme_"))
    router.message.register(get_text_query, F.text, AddQuery.text)
    router.callback_query.register(my_queries, F.data == "my_query")
    router.callback_query.register(query_profile, lambda x: x.data.startswith("query_"))
