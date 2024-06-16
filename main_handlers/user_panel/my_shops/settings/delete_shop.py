from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.commands import Database
from database.schemas.Shop import Shop
from utils import load_texts
from keyboards import InlineKeyboardMain


async def delete_shop(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    shop: Shop = data.get("shop")

    await Database.MainBot.delete_shop(shop.id)
    await callback.message.delete()
    await callback.message.answer(text=texts['delete_shop'].format(shop.username),
                                  reply_markup=await InlineKeyboardMain.ready("my_shops"))
    return await state.clear()
