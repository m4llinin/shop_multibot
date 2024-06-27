import asyncio

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from database.schemas.Category import Category
from database.schemas.Good import Good
from database.schemas.Subcategory import Subcategory
from database.schemas.Support import Support
from utils import load_texts, Cart, MyOrder


class InlineKeyboardShop:
    texts: dict = asyncio.run(load_texts())

    @classmethod
    async def categories(cls, callback: str, categories: list[Category]):
        keyboard = []
        for category in categories:
            keyboard.append([InlineKeyboardButton(text=category.name, callback_data=f"{callback}_{category.id}")])
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def subcategories(cls, callback: str, subcategories: list[Subcategory], data: str):
        keyboard, i = [], 0
        for subcategory in subcategories:
            if i % 2 == 0:
                keyboard.append(
                    [InlineKeyboardButton(text=subcategory.name, callback_data=f"{callback}_{subcategory.id}")])
            else:
                keyboard[-1].append(
                    InlineKeyboardButton(text=subcategory.name, callback_data=f"{callback}_{subcategory.id}"))
            i += 1
        keyboard.append([InlineKeyboardButton(text=cls.texts['back'], callback_data=data)])
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def goods(cls, callback: str, goods: list[Good], extra_charge: int, data: str):
        keyboard = []
        for good in goods:
            keyboard.append(
                [InlineKeyboardButton(text=f"{good.name} ⸰ {good.price * extra_charge}₽",
                                      callback_data=f"{callback}_{good.id}")])

        keyboard.append([InlineKeyboardButton(text=cls.texts['back'], callback_data=data)])
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def good_kb(cls, cart: Cart, data: str):
        if cart.good.count:
            keyboard = [
                [InlineKeyboardButton(text=cls.texts['+1'], callback_data=f"plus_1_{cart.good.id}"),
                 InlineKeyboardButton(text=f"{cart.count} шт", callback_data="just_count"),
                 InlineKeyboardButton(text=cls.texts["-1"], callback_data=f"minus_1_{cart.good.id}")],
                [InlineKeyboardButton(text=cls.texts['+10'], callback_data=f"plus_10_{cart.good.id}"),
                 InlineKeyboardButton(text=cls.texts["-10"], callback_data=f"minus_10_{cart.good.id}")]
            ]
        else:
            keyboard = []

        all_price = cart.good.price * cart.count * cart.extra_charge
        keyboard.append(
            [InlineKeyboardButton(text=cls.texts['buy'].format(all_price), callback_data=f"buy_good_{cart.good.id}")])
        # keyboard.append([InlineKeyboardButton(text=cls.texts['promo_btn'], callback_data="have_promo")])
        keyboard.append([InlineKeyboardButton(text=cls.texts['share'],
                                              url=f"https://t.me/share/url?url=https://t.me/{cart.shop_name}?start=good_{cart.good.id}")])
        keyboard.append([InlineKeyboardButton(text=cls.texts['back'], callback_data=data)])
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def pay_kb(cls, url: str, data: str):
        keyboard = [
            [InlineKeyboardButton(text=cls.texts['pay_btn'], url=url)],
            [InlineKeyboardButton(text=cls.texts['back'], callback_data=data)]
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def choose_payment(cls, data: str):
        keyboard = [
            [InlineKeyboardButton(text=cls.texts['pay_from_balance_btn'], callback_data="pay_from_balance")],
            [InlineKeyboardButton(text=cls.texts['pay_card_btn'], callback_data="pay_card")],
            [InlineKeyboardButton(text=cls.texts['back'], callback_data=data)]
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def my_profile_kb(cls):
        keyboard = [
            [InlineKeyboardButton(text=cls.texts['my_orders_btn'], callback_data="my_orders"),
             InlineKeyboardButton(text=cls.texts['update_balance_btn'], callback_data="update_balance")],
            [InlineKeyboardButton(text=cls.texts['referral_sys_btn'], callback_data="referral_sys")]
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def update_balance_btn(cls, from_profile: bool = False):
        keyboard = [
            [InlineKeyboardButton(text="100₽", callback_data="update_balance_100"),
             InlineKeyboardButton(text="250₽", callback_data="update_balance_250")],
            [InlineKeyboardButton(text="500₽", callback_data="update_balance_500"),
             InlineKeyboardButton(text="1000₽", callback_data="update_balance_1000")]
        ]

        if from_profile:
            keyboard.append([InlineKeyboardButton(text=cls.texts['back'], callback_data="my_profile")])

        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def referral(cls, link: str, user_id: int, data: str):
        keyboard = [
            [InlineKeyboardButton(text=cls.texts['share_frens'],
                                  url=f"https://t.me/share/url?url=https://t.me/{link}?start={user_id}")],
            [InlineKeyboardButton(text=cls.texts['back'], callback_data=data)],
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def my_orders(cls, my_order: MyOrder):
        keyboard = []

        start_ind = (my_order.cur_page - 1) * 3
        finish_ind = start_ind + 3 if (start_ind + 3) < len(my_order.orders) else len(my_order.orders)

        for i in range(start_ind, finish_ind):
            if my_order.orders[i].status == "paid":
                keyboard.append(
                    [InlineKeyboardButton(text=f"🟢 {my_order.orders[i].good_name}",
                                          callback_data=f"my_order_{my_order.orders[i].id}")])
            else:
                keyboard.append(
                    [InlineKeyboardButton(text=f"🔴 {my_order.orders[i].good_name}",
                                          callback_data=f"my_order_{my_order.orders[i].id}")])

        keyboard.append([InlineKeyboardButton(text=cls.texts["<"], callback_data="back_page"),
                         InlineKeyboardButton(text=cls.texts["page"].format(my_order.cur_page, my_order.all_pages),
                                              callback_data="just_page"),
                         InlineKeyboardButton(text=cls.texts[">"], callback_data="next_page")])
        keyboard.append([InlineKeyboardButton(text=cls.texts['back'], callback_data="my_profile")])
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def back(cls, data: str):
        keyboard = [
            [InlineKeyboardButton(text=cls.texts['back'], callback_data=data)],
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def support_kb(cls):
        keyboard = [
            [InlineKeyboardButton(text=cls.texts['add_query_btn'], callback_data="add_query")],
            [InlineKeyboardButton(text=cls.texts['my_query_btn'], callback_data="my_query")]
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def support_themes(cls):
        keyboard = [
            [InlineKeyboardButton(text=cls.texts['theme_1'], callback_data="theme_1")],
            [InlineKeyboardButton(text=cls.texts['theme_2'], callback_data="theme_2")],
            [InlineKeyboardButton(text=cls.texts['theme_3'], callback_data="theme_3")],
            [InlineKeyboardButton(text=cls.texts['theme_4'], callback_data="theme_4")],
            [InlineKeyboardButton(text=cls.texts['back'], callback_data="support")]
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def list_queries(cls, queries: list[Support]):
        keyboard = [[InlineKeyboardButton(text=cls.texts['add_query_btn'], callback_data="add_query")]]
        for query in queries:

            if query.status == "wait":
                emoji = "🟠"
            elif query.status == "done":
                emoji = "✅"
            else:
                emoji = "❌"

            keyboard.append([InlineKeyboardButton(text=cls.texts['schedule_query_btn'].format(emoji=emoji,
                                                                                              theme=query.theme,
                                                                                              date=query.created_at.strftime(
                                                                                                  '%d.%m.%Y %H:%M')),
                                                  callback_data=f"query_{query.id}")])
        keyboard.append([InlineKeyboardButton(text=cls.texts['back'], callback_data="support")])
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def subscribe(cls, channel: str):
        keyboard = [
            [InlineKeyboardButton(text=cls.texts['subscribe'], url=f"{channel}")],
            [InlineKeyboardButton(text=cls.texts['check'], callback_data="start")],
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def support_solution(cls, request_id: int):
        keyboard = [
            [InlineKeyboardButton(text=cls.texts['successful_payments'],
                                  callback_data=f"successful_support_{request_id}"),
             InlineKeyboardButton(text=cls.texts['bad_payments'], callback_data=f"bad_support_{request_id}")]
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)
