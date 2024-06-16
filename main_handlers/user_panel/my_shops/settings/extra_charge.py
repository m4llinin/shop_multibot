from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.schemas.Shop import Shop
from utils import load_texts
from keyboards import InlineKeyboardMain

from database.commands import Database


async def extra_charge(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    shop: Shop = data.get("shop")

    await callback.message.delete()
    return await callback.message.answer(text=texts['extra_charge'].format(shop.username, shop.extra_charge),
                                         reply_markup=await InlineKeyboardMain.extra_charge(shop.id))


async def percent(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    shop: Shop = data.get("shop")
    amount, shop_id = int(callback.data.split("_")[1]), int(callback.data.split("_")[2])

    await Database.MainBot.change_extra_charge(shop_id, amount)
    shop.extra_charge = amount
    await state.update_data(shop=shop)

    await callback.message.delete()
    return await callback.message.answer(text=texts['extra_charge'].format(shop.username, shop.extra_charge),
                                         reply_markup=await InlineKeyboardMain.extra_charge(shop.id))
