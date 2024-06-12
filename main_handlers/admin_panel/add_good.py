from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.commands import Database
from keyboards.main.inline import InlineKeyboardMain
from keyboards.shop.inline import InlineKeyboardShop
from utils import load_texts

from states.main_bot import AddGoods


async def add_good(callback: CallbackQuery, state: FSMContext):
    await state.set_state(None)
    texts = await load_texts()
    categories = await Database.ShopBot.get_categories()
    if categories:
        await callback.message.delete()
        return await callback.message.answer(text=texts['chose_categories'],
                                             reply_markup=await InlineKeyboardMain.categories("insert_subcat",
                                                                                              categories,
                                                                                              "admin_panel"))
    return await callback.answer(text=texts['no_categories'], show_alert=True)


async def insert_subcat(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    category_id = int(callback.data.split('_')[2])
    category = await Database.ShopBot.get_category_by_id(category_id)
    subcategories = await Database.ShopBot.get_subcategories(category_id)
    await state.update_data(category_id=category_id)

    data = await state.get_data()
    if "subcategory_id" in data:
        data.pop("subcategory_id")
        await state.set_data(data)

    await callback.message.delete()
    if subcategories:
        return await callback.message.answer(text=texts['choose_subcategories'].format(category=category.name),
                                             reply_markup=await InlineKeyboardMain.subcategories("insert_good",
                                                                                                 subcategories,
                                                                                                 "add_good",
                                                                                                 category_id))
    await state.set_state(AddGoods.name)
    return await callback.message.answer(text=texts['add_without_subcategories'].format(category=category.name),
                                         reply_markup=await InlineKeyboardMain.back("add_good"))


async def insert_good(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    category_id = data.get("category_id")
    subcategory_id = int(callback.data.split('_')[2])

    category = await Database.ShopBot.get_category_by_id(category_id)
    subcategory = await Database.ShopBot.get_subcategory_by_id(subcategory_id)

    await state.update_data(subcategory_id=subcategory_id)
    await state.set_state(AddGoods.name)
    await callback.message.delete()
    return await callback.message.answer(text=texts['add_good_text'].format(category=category.name,
                                                                            subcategory=subcategory.name),
                                         reply_markup=await InlineKeyboardMain.back(f"insert_subcat_{category_id}"))


async def get_good_name(message: Message, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    category_id, subcategory_id = data.get("category_id"), data.get("subcategory_id", 0)

    if not (await Database.MainBot.get_good_by_name(message.text, category_id, subcategory_id)):
        await Database.MainBot.insert_good(category_id, subcategory_id, message.text)
        await state.set_state(AddGoods.description)
        await state.update_data(name_subcategory=message.text,
                                good=await Database.MainBot.get_good_by_name(message.text, category_id, subcategory_id))
        return await message.answer(text=texts['get_name_good'].format(good=message.text))
    return await message.answer(text=texts['has_good'])


async def get_good_description(message: Message, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    good = data.get("good")

    await Database.MainBot.update_good_description(good.id, message.html_text)
    await state.set_state(AddGoods.price)
    return await message.answer(text=texts['get_description_good'].format(description=message.html_text))


async def get_good_price(message: Message, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    good = data.get("good")

    try:
        await Database.MainBot.update_good_price(good.id, int(message.text))
        await state.set_state(AddGoods.count)
        return await message.answer(text=texts['get_price_good'].format(price=message.text))
    except (ValueError, TypeError):
        return await message.answer(text=texts['bad_price'])


async def get_good_count(message: Message, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    good = data.get("good")

    try:
        if message.text.lower() == "none":
            await Database.MainBot.update_good_count(good.id, None)
        else:
            await Database.MainBot.update_good_count(good.id, int(message.text))

        await state.set_state(AddGoods.product)
        return await message.answer(text=texts['get_count_good'].format(count=message.text))
    except (ValueError, TypeError):
        return await message.answer(text=texts['bad_price'])


async def get_product(message: Message, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    good = data.get("good")

    await Database.MainBot.update_product(good.id, message.text)
    await state.set_state(None)
    return await message.answer(text=texts['get_product'], reply_markup=await InlineKeyboardMain.ready("admin_panel"))
