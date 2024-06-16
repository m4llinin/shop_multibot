from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database.commands import Database
from utils import load_texts
from keyboards import InlineKeyboardMain


async def admin_panel(message: Message):
    texts = await load_texts()
    user = await Database.MainBot.get_user(message.chat.id)
    if user.status == "admin" or user.status == "main_admin":
        return await message.answer(text=texts['admin_panel'],
                                    reply_markup=await InlineKeyboardMain.admin_kb(user.status == "main_admin"))


async def admin_panel_clb(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    user = await Database.MainBot.get_user(callback.message.chat.id)
    await state.clear()
    await callback.message.delete()
    return await callback.message.answer(text=texts['admin_panel'],
                                         reply_markup=await InlineKeyboardMain.admin_kb(user.status == "main_admin"))
