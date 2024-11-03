from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.commands import Database
from utils import load_texts
from states.main_bot import Ban
from keyboards import InlineKeyboardMain


async def ban(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    await state.set_state(Ban.username)
    await callback.message.delete()
    await callback.message.answer(text=texts['ban'],
                                  reply_markup=await InlineKeyboardMain.back("admin_panel"))


async def successful_ban(message: Message, state: FSMContext):
    texts = await load_texts()
    user = await Database.MainBot.get_user(message.text)
    if not user:
        return await message.answer(text=texts['user_not_found'],
                                    reply_markup=await InlineKeyboardMain.back("admin_panel"))

    await Database.MainBot.ban_user(user.id, not user.is_ban)
    await state.set_state(None)

    if not user.is_ban:
        return await message.answer(text=texts['successful_ban'],
                                    reply_markup=await InlineKeyboardMain.back("admin_panel"))
    return await message.answer(text=texts['successful_unban'],
                                reply_markup=await InlineKeyboardMain.back("admin_panel"))
