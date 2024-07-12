from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from keyboards.main.inline import InlineKeyboardMain
from utils import load_texts
from database.commands import Database


async def delete_category(callback: CallbackQuery):
    texts = await load_texts()
    category_id = int(callback.data.split("_")[2])
    await Database.MainBot.delete_category(category_id)

    await callback.message.delete()
    categories = await Database.ShopBot.get_categories()
    if categories:
        return await callback.message.answer(text=texts['categories'],
                                             reply_markup=await InlineKeyboardMain.categories("category",
                                                                                              categories,
                                                                                              "admin_panel"))
    return await callback.message.answer(text=texts['now_no_catalogue'],
                                         reply_markup=await InlineKeyboardMain.back("admin_panel"))


async def delete_subcategory(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    subcategory_id = int(callback.data.split("_")[2])
    data = await state.get_data()
    category_id = data.get("category_id", 0)
    await Database.MainBot.delete_subcategory(subcategory_id)

    category = await Database.ShopBot.get_category_by_id(category_id)
    subcategories = await Database.ShopBot.get_subcategories(category_id)

    await callback.message.delete()
    if subcategories:
        return await callback.message.answer(text=texts['subcategories'].format(category_name=category.name,
                                                                                category_description=category.description if category.description else ""),
                                             reply_markup=await InlineKeyboardMain.subcategories("subcategory",
                                                                                                 subcategories,
                                                                                                 "view_category",
                                                                                                 category_id))

    categories = await Database.ShopBot.get_categories()
    return await callback.message.answer(text=texts['categories'],
                                         reply_markup=await InlineKeyboardMain.categories("category",
                                                                                          categories,
                                                                                          "admin_panel"))


async def delete_good(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    texts = await load_texts()
    good_id, subcategory_id, category_id = int(callback.data.split('_')[2]), data.get("subcategory_id", 0), data.get(
        "category_id", 0)
    await Database.MainBot.delete_good(good_id)
    await callback.message.delete()

    category = await Database.ShopBot.get_category_by_id(category_id)
    subcategory = await Database.ShopBot.get_subcategory_by_id(subcategory_id)
    goods = await Database.ShopBot.get_goods(category_id, subcategory_id)

    if subcategory_id != 0:
        return await callback.message.answer(text=texts['goods_list'].format(category_name=category.name,
                                                                             subcategory_name=subcategory.name,
                                                                             subcategory_description=subcategory.description if subcategory.description else ""),
                                             reply_markup=await InlineKeyboardMain.goods("good",
                                                                                         goods,
                                                                                         f"category_{category_id}",
                                                                                         subcategory_id=subcategory_id))
    elif category_id != 0:
        return await callback.message.answer(text=texts['subcategories'].format(category_name=category.name,
                                                                                category_description=category.description if category.description else ""),
                                             reply_markup=await InlineKeyboardMain.goods("good",
                                                                                         goods,
                                                                                         f"view_category",
                                                                                         category_id=category_id))


async def delete_shop(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
