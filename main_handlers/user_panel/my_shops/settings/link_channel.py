import logging

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.schemas.Shop import Shop
from states.main_bot import LinkChannel
from utils import load_texts
from keyboards import InlineKeyboardMain

from database.commands import Database

logger = logging.getLogger(__file__)


async def link_channel(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    shop: Shop = data.get("shop")

    if shop.channel:
        count_users = await Database.MainBot.get_users_shop(shop.id)
        await Database.MainBot.change_channel(shop.id, None)
        await callback.message.delete()
        shop.channel = None
        await state.update_data(shop=shop)
        return await callback.message.answer(text=texts['shop_profile'].format(username=shop.username,
                                                                               extra_charge=shop.extra_charge),
                                             reply_markup=await InlineKeyboardMain.settings_list(shop.id,
                                                                                                 shop.notifications,
                                                                                                 count_users))

    await state.set_state(LinkChannel.channel)
    await callback.message.delete()
    return await callback.message.answer(text=texts['link_channel'].format(shop.username, shop.username),
                                         reply_markup=await InlineKeyboardMain.back(f"settings_{shop.id}"))


async def linked_channel(message: Message, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    shop: Shop = data.get("shop")

    await state.set_state(None)

    try:
        channel_id = message.forward_origin.chat.id
        shop_bot = Bot(token=shop.token, session=message.bot.session)

        channel = await shop_bot.get_chat(channel_id)
        await Database.MainBot.change_channel(shop.id, str(channel.id))

        shop.channel = str(channel_id)
        await state.update_data(shop=shop)

        return await message.answer(text=texts['successful_link'].format(shop.username, channel.full_name),
                                    reply_markup=await InlineKeyboardMain.ready(f"settings_{shop.id}"))
    except Exception as e:
        logger.error(e)
        return await message.answer(text=texts['failed_link'],
                                    reply_markup=await InlineKeyboardMain.back(f"settings_{shop.id}"))
