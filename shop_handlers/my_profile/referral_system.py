from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

from utils import load_texts
from database.commands import Database
from keyboards import InlineKeyboardShop


async def referral_system(callback: CallbackQuery):
    texts = await load_texts()

    shop = await Database.MainBot.get_shop(callback.bot.id)
    referral_count = await Database.ShopBot.get_partner_count(callback.message.chat.id, callback.bot.id)

    await callback.message.delete()
    await callback.message.answer(text=texts['referral_sys'].format(referral_count=referral_count,
                                                                    link=shop.username,
                                                                    user_id=callback.message.chat.id),
                                  reply_markup=await InlineKeyboardShop.referral(link=shop.username,
                                                                                 user_id=callback.message.chat.id,
                                                                                 data="my_profile"),
                                  parse_mode=ParseMode.HTML)
