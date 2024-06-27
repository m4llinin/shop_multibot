from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from utils import load_texts
from database.commands import Database
from keyboards import InlineKeyboardMain

from states.main_bot import Recover


async def recover(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    texts = await load_texts()
    await callback.message.delete()
    return await callback.message.answer(text=texts['recover'], reply_markup=await InlineKeyboardMain.recover_kb())


async def recover_code(callback: CallbackQuery):
    texts = await load_texts()
    user = await Database.MainBot.get_user(callback.message.chat.id)

    await callback.message.delete()
    return await callback.message.answer(text=texts['recover_code'].format(user.recover_code),
                                         reply_markup=await InlineKeyboardMain.recover_code())


async def new_recover_code(callback: CallbackQuery):
    texts = await load_texts()
    await Database.MainBot.generate_recover_code(callback.message.chat.id)
    user = await Database.MainBot.get_user(callback.message.chat.id)

    await callback.message.delete()
    return await callback.message.answer(text=texts['recover_code'].format(user.recover_code),
                                         reply_markup=await InlineKeyboardMain.recover_code())


async def recover_account(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()

    await state.set_state(Recover.code)
    await callback.message.delete()
    return await callback.message.answer(text=texts['recover_account'],
                                         reply_markup=await InlineKeyboardMain.back("recover"))


async def get_code(message: Message, state: FSMContext):
    await state.set_state(None)
    texts = await load_texts()
    recoverCode = message.text
    user = await Database.MainBot.get_user_recover_code(recoverCode)

    if user.id == message.chat.id:
        return await message.answer(text=texts['its_you'],
                                    reply_markup=await InlineKeyboardMain.back("recover_account"))

    if user is None:
        return await message.answer(text=texts['not_found'],
                                    reply_markup=await InlineKeyboardMain.back("recover_account"))

    await Database.MainBot.delete_user(recoverCode)
    await Database.MainBot.update_from_recover_code(message.chat.id, user)

    return await message.answer(text=texts['get_code'], reply_markup=await InlineKeyboardMain.ready("constructor"))
