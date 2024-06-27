from aiogram.types import CallbackQuery
from utils import load_texts
from database.commands import Database


async def successful_level(callback: CallbackQuery):
    texts = await load_texts()
    user_id, loyalty_level = int(callback.data.split("_")[2]), int(callback.data.split("_")[3])
    await Database.MainBot.update_loyalty_level(user_id, loyalty_level)
    return await callback.message.edit_message_text(text=texts['successful_level'])


async def bad_level(callback: CallbackQuery):
    texts = await load_texts()
    return await callback.message.edit_message_text(text=texts['bad_level'])
