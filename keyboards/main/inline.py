import asyncio

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from database.schemas.Category import Category
from database.schemas.Good import Good
from database.schemas.Subcategory import Subcategory
from utils import load_texts


class InlineKeyboardMain:
    texts: dict = asyncio.run(load_texts())

    @classmethod
    async def start_bk(cls):
        keyboard = [
            [InlineKeyboardButton(text=cls.texts['news_channel_btn'], url=cls.texts['news_channel_url'])]
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def menu_kb(cls, count: int):
        keyboard = [
            [InlineKeyboardButton(text=cls.texts['create_shop'], callback_data='create_shop')],
            [InlineKeyboardButton(text=cls.texts['my_shops_menu'].format(count), callback_data='my_shops')],
            [InlineKeyboardButton(text=cls.texts['mailing_lists'], callback_data='mailing_lists')],
            [InlineKeyboardButton(text=cls.texts['statistics'], callback_data='statistics')],
            [InlineKeyboardButton(text=cls.texts['withdraw_funds'], callback_data='withdraw_funds')],
            [InlineKeyboardButton(text=cls.texts['subpartnership'], callback_data='subpartnership')],
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def add_new_shop(cls):
        keyboard = [
            [InlineKeyboardButton(text=cls.texts['BotFather'], url=cls.texts['BotFather_link'])],
            [InlineKeyboardButton(text=cls.texts['back'], callback_data='constructor')],
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def back(cls, data: str):
        keyboard = [
            [InlineKeyboardButton(text=cls.texts['back'], callback_data=data)],
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def ready(cls, data: str):
        keyboard = [
            [InlineKeyboardButton(text=cls.texts['ready'], callback_data=data)],
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def admin_kb(cls):
        keyboard = [
            [InlineKeyboardButton(text=cls.texts['view_category'], callback_data='view_category')],
            [InlineKeyboardButton(text=cls.texts['add_category'], callback_data='add_category')],
            [InlineKeyboardButton(text=cls.texts['add_subcategory'], callback_data='add_subcategory')],
            [InlineKeyboardButton(text=cls.texts['add_good'], callback_data='add_good')],
            [InlineKeyboardButton(text=cls.texts['statistics'], callback_data='statistics')],
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def good_kb_admin(cls, good_id: int, data: str, count: int | None):
        if count:
            keyboard = [
                [InlineKeyboardButton(text=cls.texts['add_count'], callback_data=f'edit_good_{good_id}')]
            ]
        else:
            keyboard = []

        keyboard.append([InlineKeyboardButton(text=cls.texts['delete'], callback_data=f'delete_good_{good_id}')])
        keyboard.append([InlineKeyboardButton(text=cls.texts['back'], callback_data=data)])
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def categories(cls, callback: str, categories: list[Category], data: str):
        keyboard = []
        for category in categories:
            keyboard.append([InlineKeyboardButton(text=category.name, callback_data=f"{callback}_{category.id}")])
        keyboard.append([InlineKeyboardButton(text=cls.texts['back'], callback_data=data)])
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def subcategories(cls, callback: str, subcategories: list[Subcategory], data: str, category_id: int):
        keyboard, i = [[InlineKeyboardButton(text=cls.texts['delete'],
                                             callback_data=f'delete_category_{category_id}')]], 0
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
    async def goods(cls, callback: str, goods: list[Good], data: str, subcategory_id: int = None,
                    category_id: int = None):
        keyboard = [[InlineKeyboardButton(text=cls.texts['delete'],
                                          callback_data=f'delete_category_{category_id}' if category_id else
                                          f"delete_subcategory_{subcategory_id}")]]
        for good in goods:
            keyboard.append(
                [InlineKeyboardButton(text=f"{good.name} ⸰ {good.price}₽",
                                      callback_data=f"{callback}_{good.id}")])

        keyboard.append([InlineKeyboardButton(text=cls.texts['back'], callback_data=data)])
        return InlineKeyboardMarkup(inline_keyboard=keyboard)
