from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from utils import load_texts
from database.commands import Database
from keyboards import InlineKeyboardMain
from states.main_bot import WithdrawFunds


async def withdraw_funds(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    user = await Database.MainBot.get_user(callback.message.chat.id)
    value = 5000

    if user.balance < value:
        return await callback.answer(text=texts['not_funds'].format(value), show_alert=True)

    await state.set_state(WithdrawFunds.payment)
    await callback.message.delete()
    return await callback.message.answer(text=texts['withdraw_funds_text'],
                                         reply_markup=await InlineKeyboardMain.back("constructor"))


async def payments(message: Message, state: FSMContext):
    texts = await load_texts()
    cart_number = message.text.replace(" ", "")

    await state.update_data(cart=cart_number)
    await state.set_state(WithdrawFunds.Amount)
    return await message.answer(text=texts['get_payment'])


async def amount(message: Message, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    user = await Database.MainBot.get_user(message.chat.id)

    try:
        value = int(message.text)
        if value > user.balance:
            return await message.answer(text=texts['not_balance'])
        elif value < 5000:
            return await message.answer(text=texts['not_funds'].format(5000))
    except ValueError:
        return await message.answer(text=texts['bad_price'])

    await Database.MainBot.insert_payment(user.id, data.get("cart"), value)
    payment = await Database.MainBot.get_last_payment()

    if user.loyalty_level == 40 or (user.loyalty_level == 45 and not user.referral_id) or user.loyalty_level == 50:
        value = value - (value * 0.03)

    admin = await Database.MainBot.get_admin()
    await message.bot.send_message(chat_id=admin.id,
                                   text=texts['query_withdraw_funds'].format(user.id, data.get("cart"), value),
                                   reply_markup=await InlineKeyboardMain.solution_admin_funds(payment.id))

    await state.clear()
    await Database.MainBot.update_user_balance(payment.user_id, user.balance - payment.amount)
    return await message.answer(text=texts['success_payment'].format(payment.id))


async def successful_payments(callback: CallbackQuery):
    texts = await load_texts()
    payment_id = int(callback.data.split("_")[2])
    payment = await Database.MainBot.get_payment(payment_id)

    await Database.MainBot.update_is_paid(payment_id, True)
    await callback.message.bot.send_message(chat_id=payment.user_id, text=texts['done_payment_user'].format(payment_id))
    return await callback.message.edit_text(
        text=texts['done_payment'].format(payment.user_id, payment.cart, payment.amount))


async def bad_payments(callback: CallbackQuery):
    texts = await load_texts()
    payment_id = int(callback.data.split("_")[2])
    user = await Database.MainBot.get_user(callback.message.chat.id)
    payment = await Database.MainBot.get_payment(payment_id)

    await Database.MainBot.update_user_balance(payment.user_id, user.balance + payment.amount)
    await callback.message.bot.send_message(chat_id=payment.user_id, text=texts['bad_payment_user'].format(payment_id))
    return await callback.message.edit_text(
        text=texts['bad_payment'].format(payment.user_id, payment.cart, payment.amount))
