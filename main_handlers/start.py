from aiogram.types import Message

from utils import load_texts
from database.commands import Database
from keyboards import InlineKeyboardMain, RelpyKeyboardMain


async def start(message: Message):
    texts = await load_texts()
    await Database.MainBot.insert_user(message.chat.id)

    user = await Database.MainBot.get_user(message.chat.id)
    await message.answer(text=texts['empty_msg'], reply_markup=await RelpyKeyboardMain.start_kb(user.status == 'admin'))
    return await message.answer(text=texts['start_main'], reply_markup=await InlineKeyboardMain.start_bk())
