from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from utils import load_texts
from keyboards import InlineKeyboardMain
from database.commands import Database

from states.main_bot import Statistics


async def statistics_users(callback: CallbackQuery, state: FSMContext):
    await state.clear()

    texts = await load_texts()
    partners, subpartners = await Database.MainBot.statistics_users()
    shops = await Database.MainBot.get_all_shops()

    await state.set_state(Statistics.users)
    await callback.message.delete()
    await callback.message.answer(text=texts['statistics_users_text'].format(partners, subpartners, len(shops)),
                                  reply_markup=await InlineKeyboardMain.back("admin_statistics"))


async def get_username(message: Message, state: FSMContext):
    texts = await load_texts()
    username = message.text
    if username[0] == "@":
        username = message.text[1:]

    user = await Database.MainBot.get_user(username)
    if not user:
        return await message.answer(text=texts['user_not_found'],
                                    reply_markup=await InlineKeyboardMain.back("admin_statistics"))

    shops = await Database.MainBot.get_shops(user.id)
    shops_links = ""
    for shop in shops:
        shops_links += f"{shop.name}\n@{shop.username}"

    await state.set_state(None)
    await message.answer(text=texts['shops_links'].format(user.username, len(shops)) + shops_links,
                         reply_markup=await InlineKeyboardMain.back("admin_statistics_users"))
