from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from config.config import ADMIN_ID
from database.commands import Database
from utils import load_texts, load_settings
from keyboards import InlineKeyboardMain


async def admin_panel(message: Message):
    texts = await load_texts()
    user = await Database.MainBot.get_user(message.chat.id)
    shop = await load_settings()

    if user.status == "admin" or user.status == "main_admin" or user.id == ADMIN_ID:
        return await message.answer(text=texts['admin_panel'],
                                    reply_markup=await InlineKeyboardMain.admin_kb(
                                        user.status == "main_admin" or user.id == ADMIN_ID,
                                        shop.get("channel") != ""))


async def admin_panel_clb(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    user = await Database.MainBot.get_user(callback.message.chat.id)
    shop = await load_settings()

    await state.clear()
    await callback.message.delete()
    return await callback.message.answer(text=texts['admin_panel'],
                                         reply_markup=await InlineKeyboardMain.admin_kb(
                                             user.status == "main_admin" or user.id == ADMIN_ID,
                                             shop.get("channel") != ""))
