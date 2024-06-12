import asyncio

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from utils import load_texts


class RelpyKeyboardShop:
    texts: dict = asyncio.run(load_texts())

    @classmethod
    async def start_kb(cls):
        keyboard = [
            [KeyboardButton(text=cls.texts['catalogue']), KeyboardButton(text=cls.texts['pay_balance_reply'])],
            [KeyboardButton(text=cls.texts['my_profile']), KeyboardButton(text=cls.texts['contact'])],
        ]
        return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
