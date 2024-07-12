from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database.commands import Database
from utils import load_texts
from states.main_bot import EditSubcategory
from keyboards import InlineKeyboardMain


async def edit_subcategory(callback: CallbackQuery, state: FSMContext):
    await state.set_state(None)
    texts = await load_texts()
    subcategory_id = int(callback.data.split("_")[2])
    await callback.message.delete()
    return await callback.message.answer(text=texts['edit_subcategory'],
                                         reply_markup=await InlineKeyboardMain.edit_subcategory(subcategory_id))


async def edit_name_subcategory(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    await state.update_data(subcategory_id=int(callback.data.split("_")[3]))
    await state.set_state(EditSubcategory.name)
    await callback.message.delete()
    return await callback.message.answer(text=texts['edit_name_subcategory'],
                                         reply_markup=await InlineKeyboardMain.back(
                                             f"edit_subcategory_{int(callback.data.split('_')[3])}"))


async def get_edit_name_subcategory(message: Message, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    await state.set_state(None)

    await Database.MainBot.update_name_subcategory(data.get("subcategory_id"), message.text)
    return await message.answer(text=texts['get_edit_name_subcategory'].format(message.text),
                                reply_markup=await InlineKeyboardMain.ready(
                                    f"edit_subcategory_{data.get('subcategory_id')}"))


async def edit_description_subcategory(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    await state.update_data(subcategory_id=int(callback.data.split("_")[3]))
    await state.set_state(EditSubcategory.description)
    await callback.message.delete()
    return await callback.message.answer(text=texts['edit_description_subcategory'],
                                         reply_markup=await InlineKeyboardMain.back(
                                             f"edit_subcategory_{int(callback.data.split('_')[3])}"))


async def get_edit_description_subcategory(message: Message, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    await state.set_state(None)

    await Database.MainBot.update_description_subcategory(data.get("subcategory_id"), message.text)
    return await message.answer(text=texts['get_edit_description_subcategory'],
                                reply_markup=await InlineKeyboardMain.ready(
                                    f"edit_subcategory_{data.get('subcategory_id')}"))
