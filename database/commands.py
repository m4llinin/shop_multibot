import logging
import uuid
from datetime import datetime
from typing import Any, List

from aiohttp import web
from config.config import POSTGRES_URL, main_bot, ADMIN_ID
from .db_gino import db

from .schemas.UserMainBot import UserMainBot
from .schemas.Shop import Shop
from .schemas.Category import Category
from .schemas.Subcategory import Subcategory
from .schemas.Good import Good
from .schemas.Order import Order
from .schemas.UserShopBot import UserShopBot
from .schemas.Support import Support
from .schemas.Payment import Payment
from .schemas.Request import Request
from .schemas.Mail import Mail
from .schemas.Link import Link

from utils import load_settings, load_texts

logger = logging.getLogger(__name__)


class Database:
    @classmethod
    def setup(cls, application: web.Application):
        application.on_startup.append(cls._on_connect)
        application.on_cleanup.append(cls._on_disconnect)

    @classmethod
    async def _on_connect(cls, application: web.Application):
        await db.set_bind(POSTGRES_URL)
        logger.info("Database was connected")

        # await db.gino.drop_all()
        await db.gino.create_all()

    @classmethod
    async def _on_disconnect(cls, application: web.Application):
        if db is not None:
            logger.info("Database was disconnected")
            await db.pop_bind().close()

    class Link:
        @classmethod
        async def insert_link(cls, shop_id: int, name: str) -> Link:
            return await Link(shop_id=shop_id, name=name, code=str(uuid.uuid4()).replace("-", "")[:16]).create()

        @classmethod
        async def get_link(cls, code: str | int) -> Link:
            if isinstance(code, int):
                return await Link.query.where(Link.id == code).gino.first()
            return await Link.query.where(Link.code == code).gino.first()

        @classmethod
        async def get_link_by_name(cls, name: str) -> Link:
            return await Link.query.where(Link.name == name).gino.first()

        @classmethod
        async def get_links(cls, shop_id: int) -> List[Link]:
            return await Link.query.where(Link.shop_id == shop_id).gino.all()

        @classmethod
        async def update_profit_link(cls, code: str, profit: int):
            return await Link.update.values(profit=Link.profit + profit).where(Link.code == code).gino.status()

        @classmethod
        async def del_link(cls, link_id: int):
            return await Link.delete.where(Link.id == link_id).gino.status()

        @classmethod
        async def update_all_visits(cls, code: str):
            return await Link.update.values(all_visits=Link.all_visits + 1).where(Link.code == code).gino.status()

        @classmethod
        async def update_unique_visits(cls, code: str, visits: list[int]):
            return await Link.update.values(unique_visits=visits).where(
                Link.code == code).gino.status()

    class Mail:
        @classmethod
        async def get_all_user_mails(cls, user_id: int) -> List[Mail]:
            data = await Mail.query.where(Mail.user_id == user_id).gino.all()
            data.reverse()
            return data

        @classmethod
        async def get_all_mails(cls, shop_id: int) -> List[Mail]:
            all_mails = await Mail.query.gino.all()
            output = []
            for mail in all_mails:
                if shop_id in mail.shop_id:
                    output.append(mail)
            output.reverse()
            return output

        @classmethod
        async def insert_mail(cls, user_id: int, shop_id: list[int], mail):
            return await Mail(user_id=user_id, shop_id=shop_id, text=mail.text, photo=mail.photo,
                              keyboard=mail.keyboard, wait_date=mail.date, loop=mail.loop).create()

        @classmethod
        async def get_mail(cls, mail_id: int) -> Mail:
            return await Mail.query.where(Mail.id == mail_id).gino.first()

        @classmethod
        async def update_status(cls, mail_id: int, status: str, send: int = 0, fail: int = 0, all_send: int = 0,
                                real_date: datetime = None):
            return await (Mail.update.values(status=status, failed_send=fail, successful_send=send,
                                             all_send=all_send, real_date=real_date).where(Mail.id == mail_id).
                          gino.first())

        @classmethod
        async def get_last_mail(cls):
            return await Mail.query.order_by(Mail.id.desc()).gino.first()

        @classmethod
        async def get_waiting_mails(cls) -> list[Mail]:
            return await Mail.query.where(Mail.status == "wait").gino.all()

        @classmethod
        async def get_admin_mails(cls, user_id: int) -> list[Mail]:
            user = await Database.MainBot.get_user(user_id)
            mails = await Mail.query.order_by(Mail.wait_date.desc()).gino.all()
            output = []
            for mail in mails:
                if len(mail.shop_id) > len(user.shops):
                    output.append(mail)
            return output

        @classmethod
        async def edit_text_mail(cls, mail_id: int, text: str):
            await Mail.update.values(text=text).where(Mail.id == mail_id).gino.status()

        @classmethod
        async def edit_photo_mail(cls, mail_id: int, photo: str):
            await Mail.update.values(photo=photo).where(Mail.id == mail_id).gino.status()

    class MainBot:
        @classmethod
        async def get_all_orders_status(cls, status: str, start: datetime = None, end: datetime = None) -> list[Order]:
            if start is None and end is None:
                return await Order.query.where(Order.status == status).gino.all()
            return await Order.query.where(Order.status == status).where(Order.updated_at >= start).where(
                Order.updated_at <= end).gino.all()

        @classmethod
        async def update_loyalty_level(cls, user_id: int, loyalty_level: int):
            return await UserMainBot.update.values(loyalty_level=loyalty_level).where(
                UserMainBot.id == user_id).gino.status()

        @classmethod
        async def generate_recover_code(cls, user_id: int):
            return await UserMainBot.update.values(recover_code=str(uuid.uuid4())).where(
                UserMainBot.id == user_id).gino.status()

        @classmethod
        async def update_from_recover_code(cls, new_user_id: int, user: UserMainBot):
            return UserMainBot.update.values(refferal_id=user.referral_id, balance=user.balance,
                                             loyalty_level=user.loyalty_level, shops=user.shops,
                                             status=user.status).where(UserMainBot.id == new_user_id).gino.status()

        @classmethod
        async def delete_user(cls, recover_code: str):
            return await UserMainBot.delete.where(UserMainBot.recover_code == recover_code).gino.status()

        @classmethod
        async def get_all_shops(cls):
            return await Shop.query.gino.all()

        @classmethod
        async def statistics_users(cls):
            partners = await UserMainBot.query.where(UserMainBot.referral_id.is_(None)).gino.all()
            subpartners = await UserMainBot.query.where(UserMainBot.referral_id.isnot(None)).gino.all()
            return len(partners), len(subpartners)

        @classmethod
        async def update_owner_balance(cls, user_id: int, amount_purchase: int | float):
            user: UserMainBot = await UserMainBot.query.where(UserMainBot.id == user_id).gino.first()
            value = int(amount_purchase * (user.loyalty_level / 100))
            await UserMainBot.update.values(balance=user.balance + value).where(UserMainBot.id == user_id).gino.status()

            if user.referral_id:
                referral: UserMainBot = await UserMainBot.query.where(UserMainBot.id == user.referral_id).gino.first()

                percent = 0.2
                if user.loyalty_level == 55:
                    percent = 0.15
                elif user.loyalty_level == 60:
                    percent = 0.1

                return await UserMainBot.update.values(balance=int(referral.balance + value * percent)).where(
                    UserMainBot.id == referral.id).gino.status()

        @classmethod
        async def get_all_users_of_shop(cls, shop_id: int):
            return await UserShopBot.query.where(UserShopBot.shop_id == shop_id).gino.all()

        @classmethod
        async def get_user_recover_code(cls, recoder_code):
            return await UserMainBot.query.where(UserMainBot.recover_code == recoder_code).gino.first()

        @classmethod
        async def get_user(cls, user_id: int | str) -> UserMainBot:
            if isinstance(user_id, int):
                return await UserMainBot.query.where(UserMainBot.id == user_id).gino.first()
            return await UserMainBot.query.where(UserMainBot.username == user_id).gino.first()

        @classmethod
        async def insert_user(cls, user_id: int, username: str, referral_id: int | None = None) -> Any:
            data = await cls.get_user(user_id)
            if not data:
                shop = await load_settings()

                if shop.get("notifications", "false") == "true":
                    texts = await load_texts()

                    try:
                        admin = (await UserMainBot.query.where(UserMainBot.status == "main_admin").gino.first()).id
                    except AttributeError:
                        admin = ADMIN_ID

                    await main_bot.send_message(chat_id=admin, text=texts['new_user'].format(username))

                if referral_id:
                    return await UserMainBot(id=user_id, username=username, referral_id=referral_id,
                                             loyalty_level=50, recover_code=str(uuid.uuid4())).create()
                return await UserMainBot(id=user_id, username=username, recover_code=str(uuid.uuid4())).create()

        @classmethod
        async def update_shops(cls, user_id: int, shop: int):
            user = await cls.get_user(user_id)
            user.shops.append(shop)
            return await UserMainBot.update.values(shops=user.shops).where(UserMainBot.id == user_id).gino.status()

        @classmethod
        async def insert_shop(cls, user_id: int, shop_id: int, token: str, username: str, name: str) -> Any:
            return await Shop(id=shop_id, owner_id=user_id, token=token, username=username, name=name).create()

        @classmethod
        async def get_shop(cls, shop_id: int | str) -> Any:
            if isinstance(shop_id, int):
                return await Shop.query.where(Shop.id == shop_id).gino.first()
            return await Shop.query.where(Shop.username == shop_id).gino.first()

        @classmethod
        async def insert_category(cls, category_name: str) -> Any:
            return await Category(name=category_name).create()

        @classmethod
        async def update_description_category(cls, category_name: str | int, description: str = None) -> Any:
            if isinstance(category_name, int):
                return await Category.update.values(description=description).where(
                    Category.id == category_name).gino.status()
            return await Category.update.values(description=description).where(
                Category.name == category_name).gino.status()

        @classmethod
        async def update_weight_category(cls, category_name: str | int, index: int = 0) -> Any:
            if isinstance(category_name, int):
                return await Category.update.values(weight=index).where(Category.id == category_name).gino.status()
            return await Category.update.values(weigth=index).where(Category.name == category_name).gino.status()

        @classmethod
        async def get_category_by_name(cls, category_name: str) -> Any:
            return await Category.query.where(Category.name == category_name).gino.first()

        @classmethod
        async def get_subcategory_by_name(cls, subcategory_name: str, category_id: int) -> Any:
            return await Subcategory.query.where(Subcategory.name == subcategory_name).where(
                Subcategory.category_id == category_id).gino.first()

        @classmethod
        async def insert_subcategory(cls, subcategory_name: str, category_id: int) -> Any:
            return await Subcategory(name=subcategory_name, category_id=category_id).create()

        @classmethod
        async def update_description_subcategory(cls, subcategory_name: str | int, description: str,
                                                 category_id: int = None):
            if isinstance(subcategory_name, int):
                return await Subcategory.update.values(description=description).where(
                    Subcategory.id == subcategory_name).gino.status()
            return await Subcategory.update.values(description=description).where(
                Subcategory.name == subcategory_name).where(Subcategory.category_id == category_id).gino.status()

        @classmethod
        async def insert_good(cls, category_id: int, subcategory_id: int, name: str) -> Any:
            return await Good(category_id=category_id, subcategory_id=subcategory_id, name=name).create()

        @classmethod
        async def get_good_by_name(cls, good_name: str, category_id: int, subcategory_id: int) -> Any:
            return await Good.query.where(Good.name == good_name).where(Good.category_id == category_id).where(
                Good.subcategory_id == subcategory_id).gino.first()

        @classmethod
        async def update_good_description(cls, good_id: int, description: str) -> Any:
            return await Good.update.values(description=description).where(Good.id == good_id).gino.status()

        @classmethod
        async def update_good_price(cls, good_id: int, price: int) -> Any:
            return await Good.update.values(price=price).where(Good.id == good_id).gino.status()

        @classmethod
        async def update_good_count(cls, good_id: int, count: int | None) -> Any:
            return await Good.update.values(count=count).where(Good.id == good_id).gino.status()

        @classmethod
        async def update_product(cls, good_id: int, product: str):
            return await Good.update.values(product=product).where(Good.id == good_id).gino.status()

        @classmethod
        async def delete_good(cls, good_id: int) -> Any:
            return await Good.delete.where(Good.id == good_id).gino.status()

        @classmethod
        async def delete_category(cls, category_id: int) -> Any:
            return await Category.delete.where(Category.id == category_id).gino.status()

        @classmethod
        async def delete_subcategory(cls, subcategory_id: int) -> Any:
            return await Subcategory.delete.where(Subcategory.id == subcategory_id).gino.status()

        @classmethod
        async def get_shops(cls, user_id: int) -> Any:
            return await Shop.query.where(Shop.owner_id == user_id).gino.all()

        @classmethod
        async def update_is_on(cls, status: bool, shop_id):
            return await Shop.update.values(is_on=status).where(Shop.id == shop_id).gino.status()

        @classmethod
        async def get_profit(cls, shop_id: int, start: int | datetime = None, end: int | datetime = None) -> Any:
            if start and end:
                orders = await Order.query.where(Order.shop_id == shop_id).where(Order.created_at >= start).where(
                    Order.created_at <= end).where(Order.status == "paid").gino.all()
                if orders:
                    return sum([order.total_price for order in orders])
            else:
                orders = await Order.query.where(Order.shop_id == shop_id).where(Order.status == "paid").gino.all()
                if orders:
                    return sum([order.total_price for order in orders])
            return 0.0

        @classmethod
        async def get_sales(cls, shop_id: int, start: int | datetime = None, end: int | datetime = None):
            if start and end:
                orders = await Order.query.where(Order.shop_id == shop_id).where(Order.created_at >= start).where(
                    Order.created_at <= end).where(Order.status == "paid").gino.all()
                if orders:
                    return len(orders)
            else:
                orders = await Order.query.where(Order.shop_id == shop_id).where(Order.status == "paid").gino.all()
                if orders:
                    return len(orders)
            return 0

        @classmethod
        async def get_users_shop(cls, shop_id: int, start: int | datetime = None, end: int | datetime = None):
            if start and end:
                users = await UserShopBot.query.where(UserShopBot.shop_id == shop_id).where(
                    UserShopBot.created_at >= start).where(UserShopBot.created_at <= end).gino.all()
                if users:
                    return len(users)
            else:
                users = await UserShopBot.query.where(UserShopBot.shop_id == shop_id).gino.all()
                if users:
                    return len(users)
            return 0

        @classmethod
        async def change_notification(cls, shop_id: int, notification: bool) -> Any:
            return await Shop.update.values(notifications=notification).where(Shop.id == shop_id).gino.status()

        @classmethod
        async def change_extra_charge(cls, shop_id: int, extra_charge: int) -> Any:
            return await Shop.update.values(extra_charge=extra_charge).where(Shop.id == shop_id).gino.status()

        @classmethod
        async def change_channel(cls, shop_id: int, channel_id: str | None) -> Any:
            return await Shop.update.values(channel=channel_id).where(Shop.id == shop_id).gino.status()

        @classmethod
        async def update_token(cls, shop_id: int, token: str) -> Any:
            return await Shop.update.values(token=token).where(Shop.id == shop_id).gino.status()

        @classmethod
        async def delete_shop(cls, shop_id: int) -> Any:
            shop = await cls.get_shop(shop_id)
            user = await cls.get_user(shop.owner_id)
            user.shops.remove(shop.id)
            await UserMainBot.update.values(shops=user.shops).where(UserMainBot.id == user.id).gino.status()
            return await shop.delete()

        @classmethod
        async def get_users_shop_list(cls, shop_id: int) -> list[UserShopBot]:
            return await UserShopBot.query.where(UserShopBot.shop_id == shop_id).gino.all()

        @classmethod
        async def get_admin(cls) -> List[UserMainBot]:
            admin = await UserMainBot.query.where(UserMainBot.status == "admin").gino.all()
            main_admin = await UserMainBot.query.where(UserMainBot.status == "main_admin").gino.all()
            return admin + main_admin

        @classmethod
        async def insert_payment(cls, user_id: int, cart: str, amount: int):
            return await Payment(user_id=user_id, cart=cart, amount=amount).create()

        @classmethod
        async def get_last_payment(cls) -> Payment:
            return await Payment.query.order_by(Payment.id.desc()).gino.first()

        @classmethod
        async def update_is_paid(cls, payment_id: int, is_paid: bool) -> Any:
            return await Payment.update.values(is_paid=is_paid).where(Payment.id == payment_id).gino.status()

        @classmethod
        async def get_payment(cls, payment_id: int):
            return await Payment.query.where(Payment.id == payment_id).gino.first()

        @classmethod
        async def update_user_balance(cls, user_id: int, balance: int | float):
            return await UserMainBot.update.values(balance=balance).where(UserMainBot.id == user_id).gino.status()

        @classmethod
        async def get_subpartners(cls, user_id: int) -> List[UserMainBot]:
            return await UserMainBot.query.where(UserMainBot.referral_id == user_id).gino.all()

        @classmethod
        async def insert_request(cls, user_id: int, source: str, experience: str, platform: str):
            return await Request(user_id=user_id, source=source, experience=experience, platform=platform).create()

        @classmethod
        async def get_last_request(cls) -> Payment:
            return await Request.query.order_by(Request.id.desc()).gino.first()

        @classmethod
        async def update_status_request(cls, request_id: int, admin_id: int, status: str) -> Any:
            return await Request.update.values(status=status, admin_id=admin_id).where(
                Request.id == request_id).gino.status()

        @classmethod
        async def get_request(cls, request_id: int):
            return await Request.query.where(Request.id == request_id).gino.first()

        @classmethod
        async def update_user_status(cls, user_id: int | str, status: str):
            if isinstance(user_id, int):
                return await UserMainBot.update.values(status=status).where(UserMainBot.id == user_id).gino.status()
            return await UserMainBot.update.values(status=status).where(UserMainBot.username == user_id).gino.status()

        @classmethod
        async def get_last_support(cls, user_id: int):
            return await Support.query.order_by(Support.id.desc()).where(Support.user_id == user_id).gino.first()

        @classmethod
        async def get_support(cls, support_id: int):
            return await Support.query.where(Support.id == support_id).gino.first()

        @classmethod
        async def update_support(cls, support_id: int, status: str, admin_id: int, solution: str = None):
            return await Support.update.values(status=status, admin=admin_id, solution=solution).where(
                Support.id == support_id).gino.status()

        @classmethod
        async def get_main_admin(cls):
            return await UserMainBot.query.where(UserMainBot.status == "main_admin").gino.all()

        @classmethod
        async def update_last_offer(cls, user_id: int, date: datetime):
            return await UserMainBot.update.values(last_offer=date).where(UserMainBot.id == user_id).gino.status()

        @classmethod
        async def get_all_users(cls):
            return await UserMainBot.query.gino.all()

        @classmethod
        async def update_name_category(cls, category_id: int, name: str):
            return await Category.update.values(name=name).where(Category.id == category_id).gino.status()

        @classmethod
        async def update_name_subcategory(cls, subcategory_id: int, name: str):
            return await Subcategory.update.values(name=name).where(Subcategory.id == subcategory_id).gino.status()

        @classmethod
        async def update_good_name(cls, good_id: int, name: str):
            return await Good.update.values(name=name).where(Good.id == good_id).gino.status()

    class ShopBot:
        @classmethod
        async def get_categories(cls):
            result = await Category.query.gino.all()
            result.sort(key=lambda x: x.weight, reverse=True)
            return result

        @classmethod
        async def get_category_by_id(cls, category_id: int) -> Any:
            return await Category.query.where(Category.id == category_id).gino.first()

        @classmethod
        async def get_subcategories(cls, category_id: int):
            return await Subcategory.query.where(Subcategory.category_id == category_id).gino.all()

        @classmethod
        async def get_goods(cls, category_id: int, subcategory_id: int = 0):
            return await Good.query.where(Good.category_id == category_id).where(
                Good.subcategory_id == subcategory_id).gino.all()

        @classmethod
        async def get_good_by_id(cls, good_id: int):
            return await Good.query.where(Good.id == good_id).gino.first()

        @classmethod
        async def get_subcategory_by_id(cls, subcategory_id: int):
            return await Subcategory.query.where(Subcategory.id == subcategory_id).gino.first()

        @classmethod
        async def insert_order(cls, user_id: int, shop_id: int, good_id: int, good_name: str, total_price: int,
                               count: int = 1):
            return await Order(user_id=user_id, shop_id=shop_id, good_id=good_id, good_name=good_name,
                               total_price=total_price, count=count).create()

        @classmethod
        async def update_order_status(cls, order_id: int, status: str):
            return await Order.update.values(status=status).where(Order.id == order_id).gino.status()

        @classmethod
        async def get_shop_by_name(cls, shop_name: str):
            return await Shop.query.where(Shop.username == shop_name).gino.first()

        @classmethod
        async def get_last_order(cls):
            return await Order.query.order_by(Order.id.desc()).gino.first()

        @classmethod
        async def get_user(cls, user_id: int, shop_id: int = None) -> UserShopBot:
            if shop_id:
                return await UserShopBot.query.where(UserShopBot.id == user_id).where(
                    UserShopBot.shop_id == shop_id).gino.first()
            return await UserShopBot.query.where(UserShopBot.id == user_id).gino.first()

        @classmethod
        async def insert_user(cls, user_id: int, shop_id: int, referral_id: int | None = None, code: str | None = None):
            if not (await cls.get_user(user_id, shop_id)):
                return await UserShopBot(id=user_id, shop_id=shop_id, referral_id=referral_id, link=code).create()

        @classmethod
        async def get_partner_balance(cls, user_id: int, shop_id: int = None) -> int:
            if shop_id:
                partners = await UserShopBot.query.where(UserShopBot.referral_id == user_id).where(
                    UserShopBot.shop_id == shop_id).gino.all()
            else:
                partners = await UserShopBot.query.where(UserShopBot.referral_id == user_id).gino.all()
            if partners:
                return sum([partner.balance for partner in partners])
            return 0

        @classmethod
        async def get_partner_count(cls, user_id: int, shop_id: int = None) -> int:
            if shop_id:
                referrals = await UserShopBot.query.where(UserShopBot.referral_id == user_id).where(
                    UserShopBot.shop_id == shop_id).gino.all()
            else:
                referrals = await UserShopBot.query.where(UserShopBot.referral_id == user_id).gino.all()
            if referrals:
                return len(referrals)
            return 0

        @classmethod
        async def get_total_orders(cls, user_id: int, shop_id: int) -> int:
            orders = await Order.query.where(Order.user_id == user_id).where(Order.status == "paid").where(
                Order.shop_id == shop_id).gino.all()
            if orders:
                return len(orders)
            return 0

        @classmethod
        async def my_orders(cls, user_id: int, shop_id: int):
            return await Order.query.where(Order.user_id == user_id).where(Order.shop_id == shop_id).gino.all()

        @classmethod
        async def get_order(cls, order_id: int):
            return await Order.query.where(Order.id == order_id).gino.first()

        @classmethod
        async def update_order_msg(cls, order_id: int, msg_id: int):
            return await Order.update.values(last_message_id=msg_id).where(Order.id == order_id).gino.status()

        @classmethod
        async def update_user_balance(cls, user_id: int, balance: int | float, shop_id: int = None):
            if shop_id:
                return await UserShopBot.update.values(balance=balance).where(UserShopBot.id == user_id).where(
                    UserShopBot.shop_id == shop_id).gino.status()
            return await UserShopBot.update.values(balance=balance).where(UserShopBot.id == user_id).gino.status()

        @classmethod
        async def insert_support(cls, user_id: int, shop_id: int, theme: str, text: str):
            return await Support(user_id=user_id, shop_id=shop_id, theme=theme, text=text).create()

        @classmethod
        async def get_queries_list(cls, user_id: int, shop_id: int):
            return await Support.query.where(Support.user_id == user_id).where(
                Support.shop_id == shop_id).gino.all()

        @classmethod
        async def get_query(cls, query_id: int) -> Support:
            return await Support.query.where(Support.id == query_id).gino.first()
