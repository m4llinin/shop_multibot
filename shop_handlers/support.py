from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from config.config import main_bot
from utils import load_texts
from keyboards import InlineKeyboardShop
from states.shop_bot import AddQuery

from database.commands import Database

statuses = {
    "wait": "В процессе",
    "done": "Решено",
    "cancel": "Отменен"
}


async def support(message: Message, state: FSMContext):
    await state.clear()
    texts = await load_texts()

    return await message.answer(text=texts['support'], reply_markup=await InlineKeyboardShop.support_kb(),
                                parse_mode=ParseMode.HTML)


async def support_clb(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    texts = await load_texts()

    await callback.message.delete()
    return await callback.message.answer(text=texts['support'], reply_markup=await InlineKeyboardShop.support_kb(),
                                         parse_mode=ParseMode.HTML)


async def support_themes(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    await state.clear()
    await callback.message.delete()
    return await callback.message.answer(text=texts['add_query'],
                                         reply_markup=await InlineKeyboardShop.support_themes(),
                                         parse_mode=ParseMode.HTML)


async def select_theme_support(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    await state.update_data(theme_support=texts[callback.data])
    await state.set_state(AddQuery.text)

    await callback.message.delete()
    await callback.message.answer(text=texts['select_theme_support'].format(texts[callback.data]),
                                  reply_markup=await InlineKeyboardShop.back("add_query"),
                                  parse_mode=ParseMode.HTML)


async def get_text_query(message: Message, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()

    await Database.ShopBot.insert_support(user_id=message.chat.id,
                                          shop_id=message.bot.id,
                                          theme=data.get("theme_support"),
                                          text=message.text)

    request = await Database.MainBot.get_last_support(message.chat.id)

    admins = await Database.MainBot.get_main_admin()
    shop = await Database.MainBot.get_shop(message.bot.id)

    for admin in admins:
        await main_bot.send_message(chat_id=admin.id, text=texts['new_support'].format(user_id=message.chat.id,
                                                                                       shop_id=message.bot.id,
                                                                                       theme=data.get("theme_support"),
                                                                                       text=message.text),
                                    reply_markup=await InlineKeyboardShop.support_solution(request.id))

    await message.answer(text=texts['added_query'], parse_mode=ParseMode.HTML)
    return await state.clear()


async def my_queries(callback: CallbackQuery):
    texts = await load_texts()
    queries = await Database.ShopBot.get_queries_list(callback.message.chat.id)

    await callback.message.delete()
    await callback.message.answer(text=texts['my_queries'],
                                  reply_markup=await InlineKeyboardShop.list_queries(queries),
                                  parse_mode=ParseMode.HTML)


async def query_profile(callback: CallbackQuery):
    texts = await load_texts()
    query = await Database.ShopBot.get_query(int(callback.data.split("_")[1]))

    solution = query.solution if query.solution else "Отсуствует"
    await callback.message.delete()
    return await callback.message.answer(text=texts['query_profile'].format(theme=query.theme,
                                                                            status=statuses[query.status],
                                                                            solution=solution),
                                         parse_mode=ParseMode.HTML,
                                         reply_markup=await InlineKeyboardShop.back("my_query"))
