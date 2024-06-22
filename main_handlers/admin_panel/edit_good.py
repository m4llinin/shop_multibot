from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database.commands import Database
from utils import load_texts
from states.main_bot import EditCount
from keyboards import InlineKeyboardMain


async def edit_good_count(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    await state.set_state(EditCount.amount)
    await state.update_data(good_id=int(callback.data.split("_")[2]))
    await callback.message.delete()
    return await callback.message.answer(text=texts['edit_count_good'])


async def get_count(message: Message, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    try:
        await Database.MainBot.update_good_count(data.get("good_id"), int(message.text))
        await state.set_state(None)
        return await message.answer(text=texts['get_count_good'].format(count=message.text),
                                    reply_markup=await InlineKeyboardMain.back(f"good_{data.get('good_id')}"))
    except ValueError:
        return await message.answer(text=texts['bad_price'])
