from aiogram.types import Message, FSInputFile

from keyboards import InlineKeyboardMain


async def information(message: Message):
    return await message.answer_photo(photo=FSInputFile("./photos/information.jpeg"),
                                      reply_markup=await InlineKeyboardMain.start_bk())
