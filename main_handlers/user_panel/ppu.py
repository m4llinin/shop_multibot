import datetime

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from utils import load_texts
from database.commands import Database
from keyboards import InlineKeyboardMain

from states.main_bot import Offer


async def ppu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    texts = await load_texts()
    await callback.message.delete()
    return await callback.message.answer(text=texts['ppu'], reply_markup=await InlineKeyboardMain.ppu())


async def offer(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    user = await Database.MainBot.get_user(callback.message.chat.id)

    if user.last_offer is not None and (datetime.datetime.now() - user.last_offer).total_seconds() <= 2592000:
        return await callback.answer(text=texts['not_offer'], show_alert=True)

    await state.set_state(Offer.text)
    await callback.message.delete()
    return await callback.message.answer(text=texts['offer'], reply_markup=await InlineKeyboardMain.back("ppu"))


async def get_offer(message: Message, state: FSMContext):
    await state.clear()
    texts = await load_texts()

    main_admin = await Database.MainBot.get_main_admin()
    await Database.MainBot.update_last_offer(message.chat.id, datetime.datetime.now())
    await message.bot.send_message(chat_id=main_admin.id, text=texts['new_offer'].format(message.text))
    return await message.answer(text=texts['new_offer_user'], reply_markup=await InlineKeyboardMain.ready("ppu"))
