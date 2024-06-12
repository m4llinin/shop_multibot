from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from utils import load_texts, create_pay_link_balance, Cart
from states.shop_bot import UpdateBalance
from keyboards import InlineKeyboardShop

from database.commands import Database


async def update_balance_1(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    await state.set_state(UpdateBalance.amount)
    await callback.message.delete()
    msg = await callback.message.answer(text=texts['update_balance_1'],
                                        reply_markup=await InlineKeyboardShop.update_balance_btn(True),
                                        parse_mode=ParseMode.HTML)
    return await state.update_data(msg=msg)


async def update_balance_2(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    amount = int(callback.data.split("_")[2])
    await state.clear()

    await Database.ShopBot.insert_order(user_id=callback.message.chat.id,
                                        shop_id=callback.bot.id,
                                        good_id=0,
                                        good_name=f"Пополнение баланса на {amount}",
                                        total_price=amount)
    order = await Database.ShopBot.get_last_order()
    shop = await callback.bot.get_me()

    url = await create_pay_link_balance(amount=amount, order_id=order.id, shop_name=shop.username)

    await callback.message.delete()
    msg = await callback.message.answer(text=texts['update_balance_2'].format(amount),
                                        reply_markup=await InlineKeyboardShop.pay_kb(url, "update_balance"),
                                        parse_mode=ParseMode.HTML)
    return await Database.ShopBot.update_order_msg(order_id=order.id, msg_id=msg.message_id)


async def update_balance_1_message(message: Message, state: FSMContext):
    texts = await load_texts()
    await state.clear()
    await state.set_state(UpdateBalance.amount)
    msg = await message.answer(text=texts['update_balance_1'],
                               reply_markup=await InlineKeyboardShop.update_balance_btn(),
                               parse_mode=ParseMode.HTML)
    return await state.update_data(msg=msg)


async def update_balance_2_message(message: Message, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    msg = data.get("msg")
    try:
        amount = int(message.text)
        if amount < 50:
            return await message.answer(text="⚠️ <b>Минимальная сумма 50₽</b>", parse_mode=ParseMode.HTML)
    except ValueError:
        return await message.answer(text=texts['bad_price'])

    await state.clear()

    await Database.ShopBot.insert_order(user_id=message.chat.id,
                                        shop_id=message.bot.id,
                                        good_id=0,
                                        good_name=f"Пополнение баланса на {amount}",
                                        total_price=amount)
    order = await Database.ShopBot.get_last_order()
    shop = await message.bot.get_me()

    url = await create_pay_link_balance(amount=amount, order_id=order.id, shop_name=shop.username)

    await msg.delete()
    msg = await message.answer(text=texts['update_balance_2'].format(amount),
                               reply_markup=await InlineKeyboardShop.pay_kb(url, "update_balance"),
                               parse_mode=ParseMode.HTML)
    return await Database.ShopBot.update_order_msg(order_id=order.id, msg_id=msg.message_id)
