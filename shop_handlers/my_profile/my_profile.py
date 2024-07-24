from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.commands import Database
from keyboards import InlineKeyboardShop
from utils import load_texts


async def my_profile(message: Message, state: FSMContext):
    await state.clear()

    texts = await load_texts()
    user = await Database.ShopBot.get_user(message.chat.id, message.bot.id)
    partner_balance = await Database.ShopBot.get_partner_balance(user.id, message.bot.id)
    total_orders = await Database.ShopBot.get_total_orders(user.id, message.bot.id)

    return await message.answer(text=texts['my_profile_text'].format(user_id=user.id,
                                                                     date_registration=user.created_at.strftime(
                                                                         '%d.%m.%Y'),
                                                                     main_balance=user.balance,
                                                                     partner_balance=partner_balance,
                                                                     total_orders=total_orders),
                                reply_markup=await InlineKeyboardShop.my_profile_kb(),
                                parse_mode=ParseMode.HTML)


async def my_profile_clb(callback: CallbackQuery, state: FSMContext):
    await state.clear()

    texts = await load_texts()
    user = await Database.ShopBot.get_user(callback.message.chat.id, callback.bot.id)
    partner_balance = await Database.ShopBot.get_partner_balance(user.id, callback.bot.id)
    total_orders = await Database.ShopBot.get_total_orders(user.id, callback.bot.id)

    await callback.message.delete()
    return await callback.message.answer(text=texts['my_profile_text'].format(user_id=user.id,
                                                                              date_registration=user.created_at.strftime(
                                                                                  '%d.%m.%Y'),
                                                                              main_balance=user.balance,
                                                                              partner_balance=partner_balance,
                                                                              total_orders=total_orders),
                                         reply_markup=await InlineKeyboardShop.my_profile_kb(),
                                         parse_mode=ParseMode.HTML)
