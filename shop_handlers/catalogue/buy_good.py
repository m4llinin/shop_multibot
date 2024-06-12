from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from keyboards import InlineKeyboardShop
from database.commands import Database
from utils import load_texts, Cart, create_pay_link


async def choose_payment(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    cart: Cart | None = data.get("cart", None)
    good_id = int(callback.data.split("_")[2])

    await Database.ShopBot.insert_order(user_id=callback.message.chat.id,
                                        shop_id=callback.bot.id,
                                        good_id=good_id,
                                        good_name=cart.good.name,
                                        total_price=cart.good.price * cart.extra_charge * cart.count,
                                        count=cart.count)

    last_order = await Database.ShopBot.get_last_order()
    cart.order_id = last_order.id
    await state.update_data(cart=cart)

    await callback.message.delete()
    await callback.message.answer(text=texts['choose_payment'].format(order_id=cart.order_id,
                                                                      good=cart.good.name,
                                                                      count=cart.count,
                                                                      total_price=(cart.good.price * cart.extra_charge
                                                                                   * cart.count)),
                                  reply_markup=await InlineKeyboardShop.choose_payment(f"good_{good_id}"),
                                  parse_mode=ParseMode.HTML)


async def buy_now_prodamus(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    cart: Cart | None = data.get("cart", None)

    if cart.good.price * cart.extra_charge * cart.count < 50:
        return await callback.answer(text="Минимальная сумма для этого способа оплаты 50₽", show_alert=True)

    url = await create_pay_link(cart)

    msg = await callback.message.edit_reply_markup(
        reply_markup=await InlineKeyboardShop.pay_kb(url, f"buy_good_{cart.good.id}"))

    await Database.ShopBot.update_order_msg(cart.order_id, msg.message_id)


async def buy_now_balance(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    cart: Cart | None = data.get("cart", None)
    user = await Database.ShopBot.get_user(callback.message.chat.id)

    total_price = cart.good.price * cart.extra_charge * cart.count

    if user.balance < total_price:
        return await callback.answer(text=texts['not_balance'], show_alert=True)

    await Database.ShopBot.update_user_balance(user.id, user.balance - total_price)
    await Database.ShopBot.update_order_status(cart.order_id, "paid")

    await callback.message.delete()
    if cart.good.count is None:
        return await callback.message.answer(text=texts['deliver_product'].format(cart.good.product),
                                             parse_mode=ParseMode.HTML)
    else:
        pass
        # МЕСТО ДЛЯ ВЫДАЧИ ТОВАРА С КОЛИЧЕСТВОМ
