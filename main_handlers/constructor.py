from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from utils import load_texts
from keyboards import InlineKeyboardMain
from database.commands import Database


async def constructor(message: Message):
    texts = await load_texts()
    user = await Database.MainBot.get_user(message.chat.id)
    return await message.answer(
        text=texts['constructor'].format(id=user.id, level=user.loyalty_level, balance=user.balance),
        reply_markup=await InlineKeyboardMain.menu_kb(len(user.shops)))


async def constructor_clb(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    user = await Database.MainBot.get_user(callback.message.chat.id)

    await state.set_state(None)
    await callback.message.delete()
    return await callback.message.answer(
        text=texts['constructor'].format(id=user.id, level=user.loyalty_level, balance=user.balance),
        reply_markup=await InlineKeyboardMain.menu_kb(len(user.shops)))
