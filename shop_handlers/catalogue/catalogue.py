from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, FSInputFile

from database.commands import Database
from keyboards import InlineKeyboardShop
from utils import load_texts, Cart


async def view_category(message: Message, state: FSMContext):
    await state.clear()
    texts = await load_texts()
    categories = await Database.ShopBot.get_categories()
    if categories:
        return await message.answer_photo(photo=FSInputFile("./photos/our_goods.png"),
                                          reply_markup=await InlineKeyboardShop.categories("category",
                                                                                           categories),
                                          parse_mode=ParseMode.HTML)
    return await message.answer(text=texts['no_catalogue'], show_alert=True)


async def view_category_clb(callback: CallbackQuery):
    texts = await load_texts()
    categories = await Database.ShopBot.get_categories()
    if categories:
        await callback.message.delete()
        return await callback.message.answer_photo(photo=FSInputFile("./photos/our_goods.png"),
                                                   reply_markup=await InlineKeyboardShop.categories("category",
                                                                                                    categories),
                                                   parse_mode=ParseMode.HTML)
    return await callback.message.answer(text=texts['no_catalogue'], show_alert=True)


async def view_subcategory(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    category_id = int(callback.data.split('_')[1])
    category = await Database.ShopBot.get_category_by_id(category_id)
    subcategories = await Database.ShopBot.get_subcategories(category_id)
    shop = await Database.MainBot.get_shop(callback.bot.id)

    data = await state.get_data()
    if "subcategory_id" in data:
        data.pop("subcategory_id")
        await state.set_data(data)

    if subcategories:
        await callback.message.delete()
        await state.update_data(category_id=category_id)
        return await callback.message.answer(text=texts['subcategories'].format(category_name=category.name,
                                                                                category_description=category.description if category.description else ""),
                                             reply_markup=await InlineKeyboardShop.subcategories("subcategory",
                                                                                                 subcategories,
                                                                                                 "view_category"),
                                             parse_mode=ParseMode.HTML)
    goods = await Database.ShopBot.get_goods(category_id)
    if goods:
        extra_charge = (shop.extra_charge / 100) + 1 if shop.extra_charge != 0 else 1
        await callback.message.delete()
        await state.update_data(category_id=category_id)
        return await callback.message.answer(text=texts['subcategories'].format(category_name=category.name,
                                                                                category_description=category.description if category.description else ""),
                                             reply_markup=await InlineKeyboardShop.goods("good",
                                                                                         goods,
                                                                                         extra_charge,
                                                                                         f"view_category"),
                                             parse_mode=ParseMode.HTML)
    return await callback.answer(text=texts['no_category'], show_alert=True)


async def view_good_list(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    category_id, subcategory_id = data.get("category_id"), int(callback.data.split('_')[1])

    category = await Database.ShopBot.get_category_by_id(category_id)
    subcategory = await Database.ShopBot.get_subcategory_by_id(subcategory_id)
    goods = await Database.ShopBot.get_goods(category_id, subcategory_id)
    shop = await Database.MainBot.get_shop(callback.bot.id)

    extra_charge = (shop.extra_charge / 100) + 1 if shop.extra_charge != 0 else 1

    if goods:
        await callback.message.delete()
        await state.update_data(subcategory_id=subcategory_id)
        return await callback.message.answer(text=texts['goods_list'].format(category_name=category.name,
                                                                             subcategory_name=subcategory.name,
                                                                             subcategory_description=subcategory.description if subcategory.description else ""),
                                             reply_markup=await InlineKeyboardShop.goods("good",
                                                                                         goods,
                                                                                         extra_charge,
                                                                                         f"category_{category_id}"),
                                             parse_mode=ParseMode.HTML)
    return await callback.answer(text=texts['no_category'], show_alert=True)


async def view_good(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    good_id, subcategory_id, category_id = int(callback.data.split('_')[1]), data.get("subcategory_id", 0), data.get(
        "category_id")

    good = await Database.ShopBot.get_good_by_id(good_id)
    shop = await Database.MainBot.get_shop(callback.bot.id)
    extra_charge = (shop.extra_charge / 100) + 1 if shop.extra_charge != 0 else 1
    cart = Cart(good=good, extra_charge=extra_charge, shop_name=shop.username)
    await state.update_data(cart=cart)

    await callback.message.delete()
    return await callback.message.answer(text=texts['good'].format(good_name=good.name,
                                                                   good_description=good.description,
                                                                   price=good.price * extra_charge),
                                         reply_markup=await InlineKeyboardShop.good_kb(cart,
                                                                                       f"subcategory_{subcategory_id}" if
                                                                                       subcategory_id != 0 else
                                                                                       f"category_{category_id}"),
                                         parse_mode=ParseMode.HTML)
