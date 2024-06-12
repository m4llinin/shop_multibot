import asyncio

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils import load_texts


class RelpyKeyboardMain:
    texts: dict = asyncio.run(load_texts())

    @classmethod
    async def start_kb(cls, is_admin: bool):
        keyboard = [
            [KeyboardButton(text=cls.texts['my_shops']), KeyboardButton(text=cls.texts['information'])]
        ]
        if is_admin:
            keyboard.append([KeyboardButton(text=cls.texts['admin_panel_btn'])])
        return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
