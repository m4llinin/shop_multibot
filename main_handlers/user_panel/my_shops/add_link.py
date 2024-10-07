from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from states.main_bot import AddLink
from database.commands import Database
from utils import load_texts
from keyboards import InlineKeyboardMain


async def list_links(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    shop = data.get("shop")

    await state.set_state(None)
    links_shop = await Database.Link.get_links(shop.id)
    await callback.message.delete()
    return await callback.message.answer(text=texts['links'].format(shopname=shop.username),
                                         reply_markup=await InlineKeyboardMain.list_links(shop.id, links_shop))


async def enter_name(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    shop = data.get("shop")

    await state.set_state(AddLink.name)
    await callback.message.delete()
    return await callback.message.answer(text=texts['enter_link_name'].format(shopname=shop.username),
                                         reply_markup=await InlineKeyboardMain.back(f"links"))


async def get_enter_name(message: Message, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    shop = data.get("shop")
    name = message.text

    if await Database.Link.get_link_by_name(name):
        return await message.answer(text=texts["is_exist"], reply_markup=await InlineKeyboardMain.back("links"))

    await state.set_state(None)
    link = await Database.Link.insert_link(shop.id, name)
    return await message.answer(text=texts['get_enter_name'].format(shopname=shop.username, code=link.code),
                                reply_markup=await InlineKeyboardMain.ready("links"))


async def link(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    shop = data.get("shop")

    link = await Database.Link.get_link(int(callback.data.split("_")[2]))
    await callback.message.delete()
    await callback.message.answer(
        text=texts['link'].format(link_name=link.name, shopname=shop.username, profit=link.profit,
                                  visit=link.all_visits,
                                  unique_visit=len(link.unique_visits), code=link.code),
        reply_markup=await InlineKeyboardMain.link(link.id))


async def del_link(callback: CallbackQuery):
    texts = await load_texts()
    link_id = int(callback.data.split("_")[2])

    await Database.Link.del_link(link_id)
    await callback.message.delete()
    await callback.message.answer(text=texts['del_link_text'], reply_markup=await InlineKeyboardMain.ready("links"))
