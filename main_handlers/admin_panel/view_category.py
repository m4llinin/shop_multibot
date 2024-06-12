from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from database.commands import Database
from utils import load_texts
from keyboards import InlineKeyboardMain


async def view_category(callback: CallbackQuery):
    texts = await load_texts()
    categories = await Database.ShopBot.get_categories()
    if categories:
        await callback.message.delete()
        return await callback.message.answer(text=texts['categories'],
                                             reply_markup=await InlineKeyboardMain.categories("category",
                                                                                              categories,
                                                                                              "admin_panel"))
    return await callback.answer(text=texts['no_catalogue'], show_alert=True)


async def view_subcategory(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    category_id = int(callback.data.split('_')[1])
    category = await Database.ShopBot.get_category_by_id(category_id)
    subcategories = await Database.ShopBot.get_subcategories(category_id)

    data = await state.get_data()
    if "subcategory_id" in data:
        data.pop("subcategory_id")
        await state.set_data(data)

    if subcategories:
        await callback.message.delete()
        await state.update_data(category_id=category_id)
        return await callback.message.answer(text=texts['subcategories'].format(category_name=category.name,
                                                                                category_description=category.description if category.description else ""),
                                             reply_markup=await InlineKeyboardMain.subcategories("subcategory",
                                                                                                 subcategories,
                                                                                                 "view_category",
                                                                                                 category_id))
    goods = await Database.ShopBot.get_goods(category_id)
    if goods:
        await callback.message.delete()
        await state.update_data(category_id=category_id)
        return await callback.message.answer(text=texts['subcategories'].format(category_name=category.name,
                                                                                category_description=category.description if category.description else ""),
                                             reply_markup=await InlineKeyboardMain.goods("good",
                                                                                         goods,
                                                                                         f"view_category",
                                                                                         category_id=category_id))
    await callback.answer(text=texts['no_category'], show_alert=True)


async def view_good_list(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    category_id, subcategory_id = data.get("category_id"), int(callback.data.split('_')[1])

    category = await Database.ShopBot.get_category_by_id(category_id)
    subcategory = await Database.ShopBot.get_subcategory_by_id(subcategory_id)
    goods = await Database.ShopBot.get_goods(category_id, subcategory_id)

    if goods:
        await callback.message.delete()
        await state.update_data(subcategory_id=subcategory_id)
        return await callback.message.answer(text=texts['goods_list'].format(category_name=category.name,
                                                                             subcategory_name=subcategory.name,
                                                                             subcategory_description=subcategory.description if subcategory.description else ""),
                                             reply_markup=await InlineKeyboardMain.goods("good",
                                                                                         goods,
                                                                                         f"category_{category_id}",
                                                                                         subcategory_id=subcategory_id))
    await callback.answer(text=texts['no_category'], show_alert=True)


async def view_good(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    good_id, subcategory_id, category_id = int(callback.data.split('_')[1]), data.get("subcategory_id", 0), data.get(
        "category_id")
    good = await Database.ShopBot.get_good_by_id(good_id)

    await callback.message.delete()
    await callback.message.answer(text=texts['good_admin'].format(good_name=good.name,
                                                                  good_description=good.description,
                                                                  price=good.price,
                                                                  count=good.count),
                                  reply_markup=await InlineKeyboardMain.good_kb_admin(good_id,
                                                                                      f"subcategory_{subcategory_id}" if
                                                                                      subcategory_id != 0 else
                                                                                      f"category_{category_id}",
                                                                                      good.count))
