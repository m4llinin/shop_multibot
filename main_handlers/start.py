from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from utils import load_texts, load_settings
from database.commands import Database
from keyboards import InlineKeyboardMain, RelpyKeyboardMain


async def start(message: Message, state: FSMContext):
    texts = await load_texts()
    split_text = message.text.split(" ")

    referral_id = None
    if len(split_text) == 2:
        if int(split_text[1]) != message.chat.id:
            referral = await Database.MainBot.get_user(int(split_text[1]))
            if referral and referral.status == "linker":
                referral_id = int(split_text[1])

    shop = await load_settings()
    if shop['channel']:
        status_channel = await message.bot.get_chat_member(chat_id=shop['channel'], user_id=message.chat.id)
        if status_channel.status == "left":
            channel = await message.bot.get_chat(shop['channel'])
            await state.update_data(referral_id=referral_id)
            return message.answer(text=texts['subscribe_channel'],
                                  reply_markup=await InlineKeyboardMain.subscribe(channel.invite_link))

    await Database.MainBot.insert_user(message.chat.id, message.chat.username, referral_id)
    user = await Database.MainBot.get_user(message.chat.id)
    await message.answer(text=texts['empty_msg'], reply_markup=await RelpyKeyboardMain.start_kb(
        user.status == 'admin' or user.status == "main_admin"))
    return await message.answer(text=texts['start_main'], reply_markup=await InlineKeyboardMain.start_bk())


async def start_clb(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    user_id = callback.message.chat.id
    shop = await load_settings()
    referral_id = (await state.get_data()).get('referral_id', None)

    await callback.message.delete()

    if shop['channel']:
        status_channel = await callback.message.bot.get_chat_member(chat_id=shop['channel'], user_id=user_id)
        if status_channel.status == "left":
            channel = await callback.bot.get_chat(shop['channel'])
            return callback.message.answer(text=texts['subscribe_channel'],
                                           reply_markup=await InlineKeyboardMain.subscribe(channel.invite_link))

    await Database.MainBot.insert_user(user_id, callback.message.chat.username, referral_id)
    user = await Database.MainBot.get_user(user_id)
    await callback.message.answer(text=texts['empty_msg'], reply_markup=await RelpyKeyboardMain.start_kb(
        user.status == 'admin' or user.status == "main_admin"))
    return await callback.message.answer(text=texts['start_main'], reply_markup=await InlineKeyboardMain.start_bk())
