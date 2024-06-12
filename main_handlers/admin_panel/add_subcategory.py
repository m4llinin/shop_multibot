from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.commands import Database
from keyboards.main.inline import InlineKeyboardMain
from keyboards.shop.inline import InlineKeyboardShop
from utils import load_texts

from states.main_bot import AddSubcategory


async def add_subcategory(callback: CallbackQuery, state: FSMContext):
    await state.set_state(None)
    texts = await load_texts()
    categories = await Database.ShopBot.get_categories()
    if categories:
        await callback.message.delete()
        return await callback.message.answer(text=texts['choose_categories'],
                                             reply_markup=await InlineKeyboardShop.categories("insert_subcategory",
                                                                                              categories,
                                                                                              "admin_panel"))
    return await callback.answer(text=texts['no_categories'], show_alert=True)


async def insert_subcategory(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    category_id = int(callback.data.split('_')[2])
    category = await Database.ShopBot.get_category_by_id(category_id)

    await state.update_data(category_id=category_id)
    await state.set_state(AddSubcategory.name)
    await callback.message.delete()
    await callback.message.answer(text=texts['insert_subcategory'].format(category=category.name),
                                  reply_markup=await InlineKeyboardMain.back("add_subcategory"))


async def get_name_subcategory(message: Message, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    category_id = data['category_id']

    if not (await Database.MainBot.get_subcategory_by_name(message.text, category_id)):
        await Database.MainBot.insert_subcategory(message.text, category_id)
        await state.set_state(AddSubcategory.description)
        await state.update_data(name_subcategory=message.text)
        return await message.answer(text=texts['get_name_subcategory'].format(category=message.text),
                                    reply_markup=await InlineKeyboardMain.ready("admin_panel"))
    return await message.answer(text=texts['has_subcategory'])


async def get_description_subcategory(message: Message, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()

    await state.set_state(None)
    await Database.MainBot.update_description_subcategory(subcategory_name=data['name_subcategory'],
                                                          description=message.html_text,
                                                          category_id=data['category_id'])
    return await message.answer(text=texts['get_subcategory_description'],
                                reply_markup=await InlineKeyboardMain.back("admin_panel"))
