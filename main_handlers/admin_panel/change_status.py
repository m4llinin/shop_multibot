import re

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.commands import Database
from states.main_bot import ChangeStatus
from utils import load_texts
from keyboards import InlineKeyboardMain

statuses = {
    "main_admin": "Главный админ",
    "admin": "Админ",
    "linker": "Субпартнер",
    "super_partner": "Супер-партнер",
    "partner": "Партнер"
}


async def change_status(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    await state.set_state(ChangeStatus.user)
    await callback.message.delete()
    await callback.message.answer(text=texts['change_status_text'],
                                  reply_markup=await InlineKeyboardMain.back("admin_panel"))


async def get_username(message: Message, state: FSMContext):
    texts = await load_texts()

    username = message.text
    if username[0] == "@":
        username = message.text[1:]

    if not (await Database.MainBot.get_user(username)):
        return await message.answer(text=texts['user_not_found'],
                                    reply_markup=await InlineKeyboardMain.back("admin_panel"))

    await state.set_state(None)
    await state.update_data(username=username)

    return await message.answer(text=texts['get_username'], reply_markup=await InlineKeyboardMain.change_status())


async def get_status(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    username = data.get("username")

    await Database.MainBot.update_user_status(username, callback.data)
    await callback.message.delete()
    await callback.message.answer(text=texts['get_status'].format(username, statuses[callback.data]),
                                  reply_markup=await InlineKeyboardMain.ready("admin_panel"), )
