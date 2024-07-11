from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from utils import load_texts, load_infobase, write_infobase
from keyboards import InlineKeyboardMain

from states.main_bot import AddInfobase


async def add_infobase(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    await state.set_state(AddInfobase.question)
    await callback.message.delete()
    return await callback.message.answer(text=texts['add_infobase'],
                                         reply_markup=await InlineKeyboardMain.back("edit_infobase"))


async def get_question(message: Message, state: FSMContext):
    texts = await load_texts()
    await state.update_data(question=message.text)
    await state.set_state(AddInfobase.url)
    await message.answer(text=texts['get_question'], reply_markup=await InlineKeyboardMain.back("add_infobase"))


async def get_url(message: Message, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    await write_infobase(data['question'], message.text)
    await message.answer(text=texts['get_url'], reply_markup=await InlineKeyboardMain.ready("edit_infobase"))
