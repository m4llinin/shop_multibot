from aiogram.types import Message, FSInputFile, CallbackQuery

from keyboards import InlineKeyboardMain
from utils import load_texts


async def information(message: Message):
    return await message.answer_photo(photo=FSInputFile("./photos/information.png"),
                                      reply_markup=await InlineKeyboardMain.information())


async def information_clb(callback: CallbackQuery):
    await callback.message.delete()
    return await callback.message.answer_photo(photo=FSInputFile("./photos/information.png"),
                                               reply_markup=await InlineKeyboardMain.information())


async def faq(callback: CallbackQuery):
    texts = await load_texts()
    await callback.message.delete()
    return await callback.message.answer(text=texts['faq_text'],
                                         reply_markup=await InlineKeyboardMain.back("information"),
                                         disable_web_page_preview=True)


async def privacy_policy(callback: CallbackQuery):
    texts = await load_texts()
    await callback.message.delete()
    return await callback.message.answer(text=texts['privacy_policy'],
                                         reply_markup=await InlineKeyboardMain.back("information"),
                                         disable_web_page_preview=True)
