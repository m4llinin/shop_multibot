from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from utils import load_texts, load_infobase, write_infobase
from keyboards import InlineKeyboardMain


async def edit_infobase(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    texts = await load_texts()
    await callback.message.delete()
    return callback.message.answer(text=texts['edit_infobase'],
                                   reply_markup=await InlineKeyboardMain.edit_infobase())
