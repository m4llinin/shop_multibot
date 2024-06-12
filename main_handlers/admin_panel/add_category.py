from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from utils import load_texts
from keyboards import InlineKeyboardMain

from states.main_bot import AddCategory
from database.commands import Database


async def add_category(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    await state.set_state(AddCategory.name)
    await callback.message.delete()
    return await callback.message.answer(text=texts['add_category_text'],
                                         reply_markup=await InlineKeyboardMain.back("admin_panel"))


async def get_name_category(message: Message, state: FSMContext):
    texts = await load_texts()
    if not (await Database.MainBot.get_category_by_name(message.text)):
        await Database.MainBot.insert_category(message.text)
        await state.set_state(AddCategory.description)
        await state.update_data(name_category=message.text)
        return await message.answer(text=texts['get_name_category'].format(category=message.text),
                                    reply_markup=await InlineKeyboardMain.ready("admin_panel"))
    return await message.answer(text=texts['has_category'])


async def get_description_category(message: Message, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()

    await state.set_state(None)
    await Database.MainBot.update_description_category(category_name=data['name_category'],
                                                       description=message.html_text)
    return await message.answer(text=texts['get_category_description'],
                                reply_markup=await InlineKeyboardMain.back("admin_panel"))
