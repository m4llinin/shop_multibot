from aiogram import Bot
from aiogram.exceptions import TelegramUnauthorizedError
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, BotCommand

from config.config import main_bot, OTHER_BOTS_URL
from database.commands import Database
from keyboards import InlineKeyboardMain
from states.main_bot import AddShop
from utils import load_texts, is_bot_token


async def add_new_shop(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()

    await state.set_state(AddShop.token)
    await callback.message.delete()
    await callback.message.answer(text=texts['add_new_shop'], reply_markup=await InlineKeyboardMain.add_new_shop())


async def new_shop(message: Message, state: FSMContext):
    texts = await load_texts()
    if not (await is_bot_token(message.text)):
        return await message.answer(text=texts['error_add_new_shop'])

    new_bot = Bot(token=message.text, session=main_bot.session)

    try:
        bot_user = await new_bot.get_me()
    except TelegramUnauthorizedError:
        return await message.answer(text=texts['error_add_new_shop'])

    bot = await Database.MainBot.get_shop(bot_user.id)
    if bot:
        return await message.answer(text=texts['has_bot'])

    commands = [BotCommand(command="start", description="♻️ ВЫЗВАТЬ МЕНЮ ♻️")]
    await new_bot.set_my_commands(commands=commands)

    await new_bot.delete_webhook(drop_pending_updates=True)
    await new_bot.set_webhook(OTHER_BOTS_URL.format(bot_token=message.text))

    await Database.MainBot.insert_shop(user_id=message.chat.id,
                                       shop_id=bot_user.id,
                                       token=message.text,
                                       username=bot_user.username,
                                       name=bot_user.full_name)
    await Database.MainBot.update_shops(message.chat.id, bot_user.id)

    await state.set_state(None)
    return await message.answer(text=texts['new_shop'].format(bot_name=bot_user.username),
                                reply_markup=await InlineKeyboardMain.back('constructor'))
