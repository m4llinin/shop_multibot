import os
import sys

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database.commands import Database
from utils import load_texts
from states.main_bot import EditCategory
from keyboards import InlineKeyboardMain


async def edit_category(callback: CallbackQuery, state: FSMContext):
    await state.set_state(None)
    texts = await load_texts()
    category_id = int(callback.data.split("_")[2])
    await callback.message.delete()
    return await callback.message.answer(text=texts['edit_category'],
                                         reply_markup=await InlineKeyboardMain.edit_category(category_id))


async def edit_name_category(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    await state.update_data(category_id=int(callback.data.split("_")[2]))
    await state.set_state(EditCategory.name)
    await callback.message.delete()
    return await callback.message.answer(text=texts['edit_name_category'],
                                         reply_markup=await InlineKeyboardMain.back(
                                             f"edit_category_{int(callback.data.split('_')[2])}"))


async def get_edit_name_category(message: Message, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    await state.set_state(None)

    await Database.MainBot.update_name_category(data.get("category_id"), message.text)
    return await message.answer(text=texts['get_edit_name_category'].format(message.text),
                                reply_markup=await InlineKeyboardMain.ready(f"edit_category_{data.get('category_id')}"))


async def edit_description_category(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    await state.update_data(category_id=int(callback.data.split("_")[2]))
    await state.set_state(EditCategory.description)
    await callback.message.delete()
    return await callback.message.answer(text=texts['edit_description_category'],
                                         reply_markup=await InlineKeyboardMain.back(
                                             f"edit_category_{int(callback.data.split('_')[2])}"))


async def get_edit_description_category(message: Message, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    await state.set_state(None)

    await Database.MainBot.update_description_category(data.get("category_id"), message.html_text)
    return await message.answer(text=texts['get_edit_description_category'],
                                reply_markup=await InlineKeyboardMain.ready(f"edit_category_{data.get('category_id')}"))


async def edit_weight_category(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    await state.update_data(category_id=int(callback.data.split("_")[2]))
    await state.set_state(EditCategory.weight)
    await callback.message.delete()
    return await callback.message.answer(text=texts['edit_weight_category'],
                                         reply_markup=await InlineKeyboardMain.back(
                                             f"edit_category_{int(callback.data.split('_')[2])}"))


async def get_edit_weight_category(message: Message, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()

    try:
        await Database.MainBot.update_weight_category(data.get("category_id"), int(message.text))
        await state.set_state(None)
        return await message.answer(text=texts['get_edit_weight_category'],
                                    reply_markup=await InlineKeyboardMain.ready(
                                        f"edit_category_{data.get('category_id')}"))
    except:
        await message.answer(text=texts['bad_price'],
                             reply_markup=await InlineKeyboardMain.back(f"edit_category_{data.get('category_id')}"))


async def edit_photo_category(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    await state.update_data(category_id=int(callback.data.split("_")[2]))
    await state.set_state(EditCategory.photo)
    await callback.message.delete()
    return await callback.message.answer(text=texts['edit_photo_category'],
                                         reply_markup=await InlineKeyboardMain.photo_category(
                                             f"edit_category_{int(callback.data.split('_')[2])}"))


async def delete_photo_category(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    category_id = data.get("category_id")
    category = await Database.ShopBot.get_category_by_id(category_id)

    await Database.MainBot.update_photo_category(category_id)
    os.remove(category.photo)
    await state.set_state(None)
    await callback.message.delete()
    await callback.message.answer(text=texts['successful_delete_photo'],
                                  reply_markup=await InlineKeyboardMain.ready(f"edit_category_{category_id}"))


async def get_edit_photo_category(message: Message, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    category_id = data.get("category_id")

    await message.bot.download(message.photo[-1].file_id, f"./photos/category/{message.photo[-1].file_id}.jpg")
    await Database.MainBot.update_photo_category(category_id, f"./photos/category/{message.photo[-1].file_id}.jpg")
    await state.set_state(None)
    await message.answer(text=texts['get_edit_photo_category'],
                         reply_markup=await InlineKeyboardMain.ready(f"edit_category_{category_id}"))
