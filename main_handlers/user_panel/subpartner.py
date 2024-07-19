from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config.config import MAIN_BOT_LINK
from utils import load_texts
from database.commands import Database
from keyboards import InlineKeyboardMain

from states.main_bot import SubmitApp


async def subpartner(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    texts = await load_texts()
    user = await Database.MainBot.get_user(callback.message.chat.id)

    if user.status == "linker":
        subpartners = await Database.MainBot.get_subpartners(user.id)

        profit = 0
        for subpart in subpartners:
            for shop_id in subpart.shops:
                profit += await Database.MainBot.get_profit(shop_id, None, None)

        text = texts['sub_link'].format(referral_count=len(subpartners),
                                        profit=profit,
                                        link=MAIN_BOT_LINK,
                                        user_id=user.id)
    else:
        text = texts['subpartner']

    await callback.message.delete()
    return await callback.message.answer(text=text,
                                         reply_markup=await InlineKeyboardMain.subpartner(user.status == "linker",
                                                                                          user.id))


async def submit_app(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()

    await state.set_state(SubmitApp.source)
    await callback.message.delete()
    return await callback.message.answer(text=texts['submit_app'],
                                         reply_markup=await InlineKeyboardMain.back("subpartner"))


async def get_source(message: Message, state: FSMContext):
    texts = await load_texts()
    await state.update_data(source=message.text)

    await state.set_state(SubmitApp.experience)
    return await message.answer(text=texts['get_source'], reply_markup=await InlineKeyboardMain.back("subpartner"))


async def get_experience(message: Message, state: FSMContext):
    texts = await load_texts()
    await state.update_data(experience=message.text)

    await state.set_state(SubmitApp.platform)
    return await message.answer(text=texts['get_experience'], reply_markup=await InlineKeyboardMain.back("subpartner"))


async def get_platform(message: Message, state: FSMContext):
    texts = await load_texts()
    await state.update_data(platform=message.text)
    data = await state.get_data()

    await Database.MainBot.insert_request(user_id=message.chat.id, **data)
    request = await Database.MainBot.get_last_request()

    admins = await Database.MainBot.get_admin()
    for admin in admins:
        await message.bot.send_message(chat_id=admin.id,
                                       text=texts["request_subpartner"].format(id=request.user_id,
                                                                               source=request.source,
                                                                               experience=request.experience,
                                                                               platform=request.platform),
                                       reply_markup=await InlineKeyboardMain.solution_admin_subpartner(request.id,
                                                                                                       message.chat.username))
    await state.clear()
    return await message.answer(text=texts['get_platform'], reply_markup=await InlineKeyboardMain.ready("constructor"))


async def successful_request(callback: CallbackQuery):
    texts = await load_texts()
    requests_id = int(callback.data.split("_")[2])
    request = await Database.MainBot.get_request(requests_id)

    if request.status != "wait":
        return await callback.message.edit_text(text=texts['has_solution'])

    await Database.MainBot.update_status_request(requests_id, callback.message.chat.id, "done")
    await Database.MainBot.update_user_status(request.user_id, "linker")
    await callback.message.edit_text(text=texts['successful_request'])

    return await callback.bot.send_message(chat_id=request.user_id,
                                           text=texts['successful_request_user'])


async def bad_request(callback: CallbackQuery):
    texts = await load_texts()
    requests_id = int(callback.data.split("_")[2])
    request = await Database.MainBot.get_request(requests_id)

    if request.status != "wait":
        return await callback.message.edit_text(text=texts['has_solution'])

    await Database.MainBot.update_status_request(requests_id, callback.message.chat.id, "cancel")
    await callback.message.edit_text(text=texts['bad_request'])

    return await callback.bot.send_message(chat_id=request.user_id,
                                           text=texts['bad_request_user'])
