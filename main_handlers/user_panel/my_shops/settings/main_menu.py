from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.commands import Database
from utils import load_texts
from keyboards import InlineKeyboardMain


async def main_menu_settings(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    texts = await load_texts()
    shop = await Database.MainBot.get_shop(int(callback.data.split("_")[1]))
    await state.update_data(shop=shop)

    count_users = await Database.MainBot.get_users_shop(shop.id)
    await callback.message.delete()
    return await callback.message.answer(text=texts['shop_profile'].format(username=shop.username,
                                                                           extra_charge=shop.extra_charge),
                                         reply_markup=await InlineKeyboardMain.settings_list(shop.id,
                                                                                             shop.notifications,
                                                                                             count_users,
                                                                                             shop.channel))
