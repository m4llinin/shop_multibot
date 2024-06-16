from aiogram import Bot
from aiogram.exceptions import TelegramUnauthorizedError
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config.config import OTHER_BOTS_URL
from database.schemas.Shop import Shop
from utils import load_texts, is_bot_token

from states.main_bot import EditToken
from keyboards import InlineKeyboardMain
from database.commands import Database


async def edit_token(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    shop: Shop = data.get("shop")

    await state.set_state(EditToken.token)
    await callback.message.delete()
    await callback.message.answer(text=texts['edit_token'].format(shop.username),
                                  reply_markup=await InlineKeyboardMain.back(f"settings_{shop.id}"))


async def get_edit_token(message: Message, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    shop: Shop = data.get("shop")

    if not (await is_bot_token(message.text)):
        return await message.answer(text=texts['error_add_new_shop'])

    new_bot = Bot(token=message.text, session=message.bot.session)

    try:
        bot_user = await new_bot.get_me()
    except TelegramUnauthorizedError:
        return await message.answer(text=texts['error_add_new_shop'])

    if shop.is_on:
        await new_bot.delete_webhook()
        await new_bot.set_webhook(OTHER_BOTS_URL.format(bot_token=message.text))

    await state.set_state(None)
    await Database.MainBot.update_token(shop.id, message.text)
    await message.answer(text=texts['get_edit_token'].format(shop.username),
                         reply_markup=await InlineKeyboardMain.ready(f"settings_{shop.id}"))
