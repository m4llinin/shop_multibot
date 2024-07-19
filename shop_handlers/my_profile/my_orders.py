from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from utils import load_texts, MyOrder
from database.commands import Database
from keyboards import InlineKeyboardShop

status = {
    "paid": "Оплачен",
    "wait pay": "Не оплачен"
}


async def my_orders_list(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    orders = await Database.ShopBot.my_orders(callback.message.chat.id)

    all_pages = int(len(orders) / 3) + (len(orders) % 3 != 0) if len(orders) > 0 else 1
    my_order = MyOrder(orders=orders, all_pages=all_pages)
    await state.update_data(my_order=my_order)

    await callback.message.delete()
    await callback.message.answer(text=texts['my_orders'], reply_markup=await InlineKeyboardShop.my_orders(my_order),
                                  parse_mode=ParseMode.HTML)


async def order_profile(callback: CallbackQuery):
    texts = await load_texts()
    order_id = int(callback.data.split("_")[2])
    order = await Database.ShopBot.get_order(order_id)
    good = await Database.ShopBot.get_good_by_id(order.good_id)

    emoji = "🟢" if order.status == "paid" else "🔴"

    await callback.message.delete()

    text = texts['order_profile'].format(emoji=emoji, order_id=order.id, good_name=order.good_name, count=order.count,
                                         total_price=order.total_price, status=status[order.status])
    if order.status == "paid":
        if good and good.count is None:
            text += f"\n\nПродукт: <b>{good.product}</b>"
        elif good and good.count is not None:
            pass
            # МЕСТО ДЛЯ ВЫДАЧИ ТОВАРА С КОЛИЧЕСТВОМ
        else:
            text += f"\n\nПродукт: <b>{order.good_name}</b>"
    return await callback.message.answer(text=text,
                                         reply_markup=await InlineKeyboardShop.back("my_orders"),
                                         parse_mode=ParseMode.HTML)


async def edit_page(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    my_order: MyOrder = data.get("my_order")

    action = callback.data.split("_")[0]
    if action == "next":
        if my_order.cur_page < my_order.all_pages:
            my_order.cur_page += 1
        else:
            return callback.answer(text=texts['last_page'], show_alert=True)
    else:
        if my_order.cur_page > 1:
            my_order.cur_page -= 1
        else:
            return callback.answer(text=texts['first_page'], show_alert=True)

    await state.update_data(my_order=my_order)

    await callback.message.delete()
    await callback.message.answer(text=texts['my_orders'], reply_markup=await InlineKeyboardShop.my_orders(my_order),
                                  parse_mode=ParseMode.HTML)


async def just_page(callback: CallbackQuery):
    texts = await load_texts()
    return await callback.answer(text=texts['just_page'], show_alert=True)
