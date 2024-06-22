from aiogram.enums import ParseMode
from aiohttp import web
from aiogram import Bot

from database.commands import Database
from utils import load_texts

from config.config import session, PAYMENT_CHANNEL_ID, main_bot


async def handler_prodamus_request(request: web.Request) -> web.Response:
    data = (await request.text()).split("&")
    order_id, status, shop_name = None, None, None

    for quantity in data:
        if quantity.split("=")[0] == "order_num":
            order_id = int(quantity.split("=")[1])
        elif quantity.split("=")[0] == "payment_status":
            status = quantity.split("=")[1]
        elif quantity.split("=")[0] == "customer_extra":
            shop_name = quantity.split("=")[1]

    if status == "success":
        texts = await load_texts()
        shop = await Database.ShopBot.get_shop_by_name(shop_name)
        order = await Database.ShopBot.get_order(order_id)
        good = await Database.ShopBot.get_good_by_id(order.good_id)
        bot = Bot(token=shop.token, session=session)

        if shop.notifications:
            await bot.send_message(chat_id=shop.owner_id, text=texts['new_purchase'].format(user_id=order.user_id,
                                                                                            order=order.id,
                                                                                            price=order.total_price))

        await Database.ShopBot.update_order_status(order_id, "paid")
        await Database.MainBot.update_owner_balance(shop.owner_id, order.total_price)

        await bot.delete_message(chat_id=order.user_id, message_id=order.last_message_id)

        if good.count is None:
            await bot.send_message(chat_id=order.user_id,
                                   text=texts['deliver_product'].format(good.product),
                                   parse_mode=ParseMode.HTML)
        else:
            pass
            # МЕСТО ДЛЯ ВЫДАЧИ ТОВАРА С КОЛИЧЕСТВОМ

        await main_bot.send_message(chat_id=PAYMENT_CHANNEL_ID, text=texts['new_purchase'].format(user_id=order.user_id,
                                                                                                  order=order.id,
                                                                                                  price=order.total_price))

    return web.Response()


async def handler_prodamus_update_balance(request: web.Request) -> web.Response:
    data = (await request.text()).split("&")
    order_id, status, shop_name, amount = None, None, None, None

    for quantity in data:
        if quantity.split("=")[0] == "order_num":
            order_id = int(quantity.split("=")[1])
        elif quantity.split("=")[0] == "payment_status":
            status = quantity.split("=")[1]
        elif quantity.split("=")[0] == "customer_extra":
            shop_name = quantity.split("=")[1]
        elif quantity.split("=")[0] == "sum":
            amount = int(quantity.split("=")[1])

    if status == "success":
        texts = await load_texts()
        shop = await Database.ShopBot.get_shop_by_name(shop_name)
        order = await Database.ShopBot.get_order(order_id)
        user = await Database.ShopBot.get_user(order.user_id)
        bot = Bot(token=shop.token, session=session)

        if shop.notifications:
            await bot.send_message(chat_id=shop.owner_id, text=texts['new_purchase'].format(user_id=order.user_id,
                                                                                            order=order.id,
                                                                                            price=order.total_price))

        await Database.ShopBot.update_order_status(order_id, "paid")
        await Database.ShopBot.update_user_balance(user.id, user.balance + amount)
        await Database.MainBot.update_owner_balance(shop.owner_id, amount)

        await bot.delete_message(chat_id=order.user_id, message_id=order.last_message_id)
        await bot.send_message(chat_id=order.user_id,
                               text=texts['successful_update_balance'].format(amount, user.balance + amount),
                               parse_mode=ParseMode.HTML)

        await main_bot.send_message(chat_id=PAYMENT_CHANNEL_ID, text=texts['new_purchase'].format(user_id=order.user_id,
                                                                                                  order=order.id,
                                                                                                  price=order.total_price))

    return web.Response()
