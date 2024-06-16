from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from utils import load_texts
from database.commands import Database
from keyboards import InlineKeyboardMain


async def my_shops(callback: CallbackQuery):
    texts = await load_texts()

    shops = await Database.MainBot.get_shops(callback.message.chat.id)
    await callback.message.delete()
    return await callback.message.answer(text=texts['my_shops_text'],
                                         reply_markup=await InlineKeyboardMain.my_shops(shops))


async def my_shops_list(callback: CallbackQuery):
    texts = await load_texts()

    shops = await Database.MainBot.get_shops(callback.message.chat.id)
    out = "\n\n".join([f"@{shop.username}" for shop in shops])
    await callback.message.edit_text(text=texts['my_shops_list'] + out,
                                     reply_markup=await InlineKeyboardMain.back("my_shops"))


async def shop_profile(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    shop = await Database.MainBot.get_shop(int(callback.data.split("_")[1]))
    await state.update_data(shop=shop)

    await callback.message.delete()
    return await callback.message.answer(text=texts['shop_profile'].format(username=shop.username,
                                                                           extra_charge=shop.extra_charge),
                                         reply_markup=await InlineKeyboardMain.shop_profile(shop.id, shop.is_on))
