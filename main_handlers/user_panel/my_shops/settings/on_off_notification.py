from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.commands import Database
from database.schemas.Shop import Shop
from utils import load_texts
from keyboards import InlineKeyboardMain


async def on_off_notification(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    shop: Shop = data.get("shop")

    count_users = await Database.MainBot.get_users_shop(shop.id)
    await Database.MainBot.change_notification(shop.id, not shop.notifications)
    shop.notifications = not shop.notifications
    await state.update_data(shop=shop)
    await callback.message.delete()
    return await callback.message.answer(text=texts['shop_profile'].format(username=shop.username,
                                                                           extra_charge=shop.extra_charge),
                                         reply_markup=await InlineKeyboardMain.settings_list(shop.id,
                                                                                             shop.notifications,
                                                                                             count_users,
                                                                                             shop.channel))
