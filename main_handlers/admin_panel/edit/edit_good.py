from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database.commands import Database
from utils import load_texts
from states.main_bot import EditGood
from keyboards import InlineKeyboardMain


async def edit_good_count(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    await state.set_state(EditGood.count)
    await state.update_data(good_id=int(callback.data.split("_")[3]))
    await callback.message.delete()
    return await callback.message.answer(text=texts['edit_count_good'],
                                         reply_markup=await InlineKeyboardMain.back(
                                             f'good_{callback.data.split("_")[3]}'))


async def get_edit_good_count(message: Message, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    try:
        await Database.MainBot.update_good_count(data.get("good_id"), int(message.text))
        await state.set_state(None)
        return await message.answer(text=texts['get_edit_good_count'].format(message.text),
                                    reply_markup=await InlineKeyboardMain.ready(f"good_{data.get('good_id')}"))
    except ValueError:
        return await message.answer(text=texts['bad_price'])


async def edit_good_price(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    await state.set_state(EditGood.price)
    await state.update_data(good_id=int(callback.data.split("_")[3]))
    await callback.message.delete()
    return await callback.message.answer(text=texts['edit_good_price'],
                                         reply_markup=await InlineKeyboardMain.back(
                                             f'good_{callback.data.split("_")[3]}'))


async def get_edit_good_price(message: Message, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    try:
        await Database.MainBot.update_good_price(data.get("good_id"), int(message.text))
        await state.set_state(None)
        return await message.answer(text=texts['get_edit_good_price'].format(message.text),
                                    reply_markup=await InlineKeyboardMain.ready(f"good_{data.get('good_id')}"))
    except ValueError:
        return await message.answer(text=texts['bad_price'])


async def edit_good_name(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    await state.update_data(good_id=int(callback.data.split("_")[3]))
    await state.set_state(EditGood.name)
    await callback.message.delete()
    return await callback.message.answer(text=texts['edit_good_name'],
                                         reply_markup=await InlineKeyboardMain.back(
                                             f"good_{int(callback.data.split('_')[3])}"))


async def get_edit_good_name(message: Message, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    await state.set_state(None)

    await Database.MainBot.update_good_name(data.get("good_id"), message.text)
    return await message.answer(text=texts['get_edit_good_name'].format(message.text),
                                reply_markup=await InlineKeyboardMain.ready(f"good_{data.get('good_id')}"))


async def edit_good_description(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    await state.update_data(good_id=int(callback.data.split("_")[3]))
    await state.set_state(EditGood.description)
    await callback.message.delete()
    return await callback.message.answer(text=texts['edit_good_description'],
                                         reply_markup=await InlineKeyboardMain.back(
                                             f"good_{int(callback.data.split('_')[3])}"))


async def get_edit_good_description(message: Message, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    await state.set_state(None)

    await Database.MainBot.update_good_description(data.get("good_id"), message.text)
    return await message.answer(text=texts['get_edit_good_description'],
                                reply_markup=await InlineKeyboardMain.ready(
                                    f"good_{data.get('good_id')}"))


async def edit_good_product(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    await state.update_data(good_id=int(callback.data.split("_")[3]))
    await state.set_state(EditGood.product)
    await callback.message.delete()
    return await callback.message.answer(text=texts['edit_good_product'],
                                         reply_markup=await InlineKeyboardMain.back(
                                             f"good_{int(callback.data.split('_')[3])}"))


async def get_edit_good_product(message: Message, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    await state.set_state(None)

    await Database.MainBot.update_product(data.get("good_id"), message.text)
    return await message.answer(text=texts['get_edit_good_product'].format(message.text),
                                reply_markup=await InlineKeyboardMain.ready(f"good_{data.get('good_id')}"))
