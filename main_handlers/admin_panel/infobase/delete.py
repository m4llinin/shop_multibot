from aiogram.types import CallbackQuery

from utils import load_texts, write_infobase
from keyboards import InlineKeyboardMain


async def delete_infobase(callback: CallbackQuery):
    texts = await load_texts()
    await callback.message.delete()
    await callback.message.answer(text=texts['delete_infobase'],
                                  reply_markup=await InlineKeyboardMain.delete_infobase())


async def delete_key(callback: CallbackQuery):
    texts = await load_texts()
    await write_infobase(callback.data)
    await callback.message.delete()
    return await callback.message.answer(text=texts['delete_key'],
                                         reply_markup=await InlineKeyboardMain.ready("edit_infobase"))
