from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from config.config import OTHER_BOTS_URL
from database.commands import Database
from database.schemas.Shop import Shop
from keyboards.main.inline import InlineKeyboardMain

from utils import load_texts


async def on_off(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    shop: Shop = data.get("shop")
    status, shop_id = callback.data.split('_')

    shop_bot = Bot(token=shop.token, session=callback.bot.session)

    if status == "off":
        await shop_bot.delete_webhook(drop_pending_updates=True)

    elif status == "on":
        await shop_bot.delete_webhook(drop_pending_updates=True)
        await shop_bot.set_webhook(OTHER_BOTS_URL.format(bot_token=shop.token))

    await Database.MainBot.update_is_on(status == "on", int(shop_id))
    await callback.message.delete()
    return await callback.message.answer(text=texts['shop_profile'].format(username=shop.username,
                                                                           extra_charge=shop.extra_charge),
                                         reply_markup=await InlineKeyboardMain.shop_profile(shop_id, status == "on"))
