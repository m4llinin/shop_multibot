from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.commands import Database
from utils import load_texts
from states.main_bot import UpdateBalance
from keyboards import InlineKeyboardMain


async def update_balance_user(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    await state.set_state(UpdateBalance.username)
    await callback.message.delete()
    await callback.message.answer(text=texts['update_balance_user'],
                                  reply_markup=await InlineKeyboardMain.back("admin_panel"))


async def update_balance_username(message: Message, state: FSMContext):
    texts = await load_texts()
    user = await Database.MainBot.get_user(message.text)
    if not user:
        return await message.answer(text=texts['user_not_found'],
                                    reply_markup=await InlineKeyboardMain.back("admin_panel"))

    await state.update_data(user_id=user.id, user_balance=user.balance)
    await state.set_state(UpdateBalance.balance)
    await message.answer(text=texts['update_balance_amount'].format(username=user.username, amount=user.balance),
                         reply_markup=await InlineKeyboardMain.back("admin_panel"))


async def update_balance(message: Message, state: FSMContext):
    texts = await load_texts()
    try:
        amount = int(message.text)
        data = await state.get_data()
        user_id = data.get('user_id')
        user_balance = data.get('user_balance')
        await Database.MainBot.update_user_balance(user_id=user_id, balance=user_balance + amount)
        await state.set_state(None)
        await message.answer(text=texts['successful_update'],
                             reply_markup=await InlineKeyboardMain.ready("admin_panel"))
    except ValueError:
        await message.answer(text=texts['bad_price'], reply_markup=await InlineKeyboardMain.back("admin_panel"))
