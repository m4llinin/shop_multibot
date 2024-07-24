import calendar
import logging
from datetime import datetime, timedelta

from aiogram.enums import ParseMode
from aiohttp import web
from aiogram import Bot

from database.commands import Database
from utils import load_texts

from keyboards import InlineKeyboardMain
from config.config import session, main_bot

logger = logging.getLogger(__name__)


async def handler_prodamus_request(request: web.Request) -> web.Response:
    try:
        data = (await request.text()).split("&")
        order_id, status, shop_name = None, None, None

        for quantity in data:
            if quantity.split("=")[0] == "order_num":
                order_id = int(quantity.split("=")[1])
            elif quantity.split("=")[0] == "payment_status":
                status = quantity.split("=")[1]
            elif quantity.split("=")[0] == "customer_extra":
                shop_name = quantity.split("=")[1]

        if status == "success" and order_id and shop_name:
            texts = await load_texts()
            shop = await Database.ShopBot.get_shop_by_name(shop_name)
            order = await Database.ShopBot.get_order(order_id)
            good = await Database.ShopBot.get_good_by_id(order.good_id)
            bot = Bot(token=shop.token, session=session)

            if shop.notifications:
                await main_bot.send_message(chat_id=shop.owner_id,
                                            text=texts['new_purchase'].format(shop=shop.username,
                                                                              user_id=order.user_id,
                                                                              good=good.name,
                                                                              price=order.total_price,
                                                                              date=datetime.now().strftime(
                                                                                  "%d.%m.%Y %H:%M")))

            user = await Database.ShopBot.get_user(order.user_id, shop.id)
            referral = None
            if user.referral_id:
                referral = await Database.ShopBot.get_user(user.referral_id, shop.id)
            if referral:
                await Database.ShopBot.update_user_balance(referral.id, referral.balance + order.total_price * 0.05,
                                                           shop.id)

            await Database.ShopBot.update_order_status(order_id, "paid")
            await Database.MainBot.update_owner_balance(shop.owner_id, order.total_price)

            owner_shop = await Database.MainBot.get_user(shop.owner_id)
            now = datetime.now()
            period = now - timedelta(days=calendar.monthrange(now.year, now.month)[1])
            start = datetime(period.year, period.month, 1, 0, 0, 1)
            end = datetime(period.year, period.month, calendar.monthrange(period.year, period.month)[1], 23, 59, 59)
            profit = sum([await Database.MainBot.get_profit(shop, start, end) for shop in owner_shop.shops])

            if profit > 50000 and owner_shop.loyalty_level == 45:
                await Database.MainBot.update_loyalty_level(owner_shop.id, 50)

            if owner_shop.referral_id and owner_shop.loyalty_level >= 50:
                if profit > 150000:
                    admins = await Database.MainBot.get_admin()
                    for admin in admins:
                        await main_bot.send_message(chat_id=admin.id,
                                                    text=texts['loyalty_level'].format(owner_shop.username, profit, 60),
                                                    reply_markup=await InlineKeyboardMain.loyalty_solution(
                                                        owner_shop.id, 60))
                elif profit > 100000:
                    admins = await Database.MainBot.get_admin()
                    for admin in admins:
                        await main_bot.send_message(chat_id=admin.id,
                                                    text=texts['loyalty_level'].format(owner_shop.username, profit, 55),
                                                    reply_markup=await InlineKeyboardMain.loyalty_solution(
                                                        owner_shop.id, 55))
            try:
                await bot.delete_message(chat_id=order.user_id, message_id=order.last_message_id)
            except Exception as e:
                logger.error(e)

            if good.count is None:
                await bot.send_message(chat_id=order.user_id,
                                       text=texts['deliver_product'].format(good.product),
                                       parse_mode=ParseMode.HTML)
            else:
                pass
                # МЕСТО ДЛЯ ВЫДАЧИ ТОВАРА С КОЛИЧЕСТВОМ
    except Exception as e:
        logger.error(e)
    return web.Response()


async def handler_prodamus_update_balance(request: web.Request) -> web.Response:
    try:
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

        if status == "success" and order_id and shop_name and amount:
            texts = await load_texts()
            shop = await Database.ShopBot.get_shop_by_name(shop_name)
            order = await Database.ShopBot.get_order(order_id)
            bot = Bot(token=shop.token, session=session)

            if shop.notifications:
                await main_bot.send_message(chat_id=shop.owner_id,
                                            text=texts['new_purchase'].format(shop=shop.username,
                                                                              user_id=order.user_id,
                                                                              good=f"Пополнение баланса на {amount}₽",
                                                                              price=order.total_price,
                                                                              date=datetime.now().strftime(
                                                                                  "%d.%m.%Y %H:%M")))

            user = await Database.ShopBot.get_user(order.user_id, shop.id)
            referral = None
            if user.referral_id:
                referral = await Database.ShopBot.get_user(user.referral_id, shop.id)
            if referral:
                await Database.ShopBot.update_user_balance(referral.id, referral.balance + order.total_price * 0.05,
                                                           shop.id)

            await Database.ShopBot.update_order_status(order_id, "paid")
            await Database.ShopBot.update_user_balance(user.id, user.balance + amount, shop.id)
            await Database.MainBot.update_owner_balance(shop.owner_id, amount)

            owner_shop = await Database.MainBot.get_user(shop.owner_id)
            now = datetime.now()
            period = now - timedelta(days=calendar.monthrange(now.year, now.month)[1])
            start = datetime(period.year, period.month, 1, 0, 0, 1)
            end = datetime(period.year, period.month, calendar.monthrange(period.year, period.month)[1], 23, 59, 59)
            profit = sum([await Database.MainBot.get_profit(shop, start, end) for shop in owner_shop.shops])

            if profit > 50000 and owner_shop.loyalty_level == 45:
                await Database.MainBot.update_loyalty_level(owner_shop.id, 50)

            if owner_shop.referral_id and owner_shop.loyalty_level >= 50:
                if profit > 150000:
                    admins = await Database.MainBot.get_admin()
                    for admin in admins:
                        await main_bot.send_message(chat_id=admin.id,
                                                    text=texts['loyalty_level'].format(owner_shop.username, profit, 60),
                                                    reply_markup=await InlineKeyboardMain.loyalty_solution(
                                                        owner_shop.id, 60))
                elif profit > 100000:
                    admins = await Database.MainBot.get_admin()
                    for admin in admins:
                        await main_bot.send_message(chat_id=admin.id,
                                                    text=texts['loyalty_level'].format(owner_shop.username, profit, 55),
                                                    reply_markup=await InlineKeyboardMain.loyalty_solution(
                                                        owner_shop.id, 55))

            try:
                await bot.delete_message(chat_id=order.user_id, message_id=order.last_message_id)
                await bot.send_message(chat_id=order.user_id,
                                       text=texts['successful_update_balance'].format(amount, user.balance + amount),
                                       parse_mode=ParseMode.HTML)
            except Exception as e:
                logger.error(e)
    except Exception as e:
        logger.error(e)

    return web.Response()
