from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from utils import load_texts
from keyboards import InlineKeyboardMain


async def statistics_menu(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    await state.clear()
    await callback.message.delete()
    return await callback.message.answer(text=texts['statistics_menu'],
                                         reply_markup=await InlineKeyboardMain.statistics_menu())
