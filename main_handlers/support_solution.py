from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from config.config import session
from database.schemas.Support import Support
from utils import load_texts
from keyboards import InlineKeyboardMain
from database.commands import Database
from states.main_bot import SupportSolution


async def successful_support(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    support_id = int(callback.data.split("_")[2])
    support = await Database.MainBot.get_support(support_id)

    if support.status == "cancel" or support.status == "done":
        return await callback.message.edit_text(text=texts['has_solution'])

    await state.update_data(support=support)
    await state.set_state(SupportSolution.text)
    await callback.message.delete()
    await callback.message.answer(text=texts['enter_solution'])


async def get_solution(message: Message, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    support: Support = data.get("support")

    if support.status == "cancel" or support.status == "done":
        await state.clear()
        return await message.answer(text=texts['has_solution'])
    await state.clear()

    await Database.MainBot.update_support(support.id, "done", message.chat.id, message.text)

    await message.answer(text=texts['successful_support'].format(message.text))

    shop = await Database.MainBot.get_shop(support.shop_id)
    bot = Bot(token=shop.token, session=session)
    return await bot.send_message(chat_id=support.user_id,
                                  text=texts['user_successful_support'].format(support_id=support.id,
                                                                               theme=support.theme,
                                                                               solution=message.text),
                                  parse_mode="HTML")


async def bad_support(callback: CallbackQuery):
    texts = await load_texts()
    support_id = int(callback.data.split("_")[2])
    support = await Database.MainBot.get_support(support_id)

    if support.status == "cancel" or support.status == "done":
        return await callback.message.edit_text(text=texts['has_solution'])

    shop = await Database.MainBot.get_shop(support.shop_id)
    bot = Bot(token=shop.token, session=session)

    await Database.MainBot.update_support(support_id, "cancel", callback.message.chat.id)

    await callback.message.edit_text(text=texts['bad_request'])
    return await bot.send_message(chat_id=support.user_id, text=texts['bad_support'].format(support_id),
                                  parse_mode="HTML")
