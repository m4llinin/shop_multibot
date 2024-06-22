import logging

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.commands import Database
from states.main_bot import LinkChannelAdmin
from utils import load_texts, load_settings, write_settings
from keyboards import InlineKeyboardMain

from config.config import MAIN_BOT_LINK, ADMIN_ID

logger = logging.getLogger(__file__)


async def link_channel(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    shop = await load_settings()

    if shop.get("channel"):
        user = await Database.MainBot.get_user(callback.message.chat.id)
        await write_settings(channel="")

        await callback.message.delete()
        return await callback.message.answer(text=texts['admin_panel'],
                                             reply_markup=await InlineKeyboardMain.admin_kb(
                                                 user.status == "main_admin" or user.id == ADMIN_ID,
                                                 False))

    await state.set_state(LinkChannelAdmin.channel)
    await callback.message.delete()
    return await callback.message.answer(text=texts['link_channel_admin'].format(MAIN_BOT_LINK),
                                         reply_markup=await InlineKeyboardMain.back("admin_panel"))


async def linked_channel(message: Message, state: FSMContext):
    texts = await load_texts()

    await state.set_state(None)

    try:
        channel_id = message.forward_origin.chat.id
        channel = await message.bot.get_chat(channel_id)
        await write_settings(channel=channel_id)

        return await message.answer(text=texts['successful_link'].format(MAIN_BOT_LINK, channel.full_name),
                                    reply_markup=await InlineKeyboardMain.ready("admin_panel"))
    except Exception as e:
        logger.error(e)
        return await message.answer(text=texts['failed_link'],
                                    reply_markup=await InlineKeyboardMain.back("admin_panel"))
