import asyncio

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from database.schemas.Category import Category
from database.schemas.Good import Good
from database.schemas.Mail import Mail
from database.schemas.Shop import Shop
from database.schemas.Subcategory import Subcategory
from utils import load_texts

from config.config import MAIN_BOT_LINK
from utils import MyMail


class InlineKeyboardMain:
    texts: dict = asyncio.run(load_texts())

    @classmethod
    async def start_bk(cls):
        keyboard = [
            [InlineKeyboardButton(text=cls.texts['news_channel_btn'], url=cls.texts['news_channel_url'])]
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def menu_kb(cls, count: int):
        keyboard = [
            [InlineKeyboardButton(text=cls.texts['create_shop'], callback_data='create_shop')],
            [InlineKeyboardButton(text=cls.texts['my_shops_menu'].format(count), callback_data='my_shops')],
            [InlineKeyboardButton(text=cls.texts['mailing_lists'], callback_data='all_mailing_list')],
            [InlineKeyboardButton(text=cls.texts['all_statistics'], callback_data='allStatistics_1')],
            [InlineKeyboardButton(text=cls.texts['withdraw_funds'], callback_data='withdraw_funds')],
            [InlineKeyboardButton(text=cls.texts['subpartnership'], callback_data='subpartner')],
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def add_new_shop(cls):
        keyboard = [
            [InlineKeyboardButton(text=cls.texts['BotFather'], url=cls.texts['BotFather_link'])],
            [InlineKeyboardButton(text=cls.texts['back'], callback_data='constructor')],
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def back(cls, data: str):
        keyboard = [
            [InlineKeyboardButton(text=cls.texts['back'], callback_data=data)],
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def ready(cls, data: str):
        keyboard = [
            [InlineKeyboardButton(text=cls.texts['ready'], callback_data=data)],
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def change_status(cls):
        keyboard = [
            [InlineKeyboardButton(text=cls.texts['main_admin'], callback_data='main_admin')],
            [InlineKeyboardButton(text=cls.texts['admin'], callback_data='admin')],
            [InlineKeyboardButton(text=cls.texts['linker'], callback_data='linker')],
            [InlineKeyboardButton(text=cls.texts['super_partner'], callback_data='super_partner')],
            [InlineKeyboardButton(text=cls.texts['partner'], callback_data='partner')],
            [InlineKeyboardButton(text=cls.texts['back'], callback_data="admin_panel")]
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def admin_kb(cls, main_admin: bool, is_linked: bool):
        keyboard = [
            [InlineKeyboardButton(text=cls.texts['all_statistics'], callback_data='admin_statistics')],
        ]
        if main_admin:
            keyboard.append([InlineKeyboardButton(text=cls.texts['view_category'], callback_data='view_category')])
            keyboard.append([InlineKeyboardButton(text=cls.texts['add_category'], callback_data='add_category')])
            keyboard.append([InlineKeyboardButton(text=cls.texts['add_subcategory'], callback_data='add_subcategory')])
            keyboard.append([InlineKeyboardButton(text=cls.texts['add_good'], callback_data='add_good')])

            keyboard.append([InlineKeyboardButton(text=cls.texts['change_status'], callback_data='change_status')])

            channel_text = cls.texts['unlink_btn'] if is_linked else cls.texts['link_btn']
            keyboard.append([InlineKeyboardButton(text=channel_text, callback_data='link_channel')])

        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def good_kb_admin(cls, good_id: int, data: str, count: int | None):
        if count:
            keyboard = [
                [InlineKeyboardButton(text=cls.texts['add_count'], callback_data=f'edit_good_{good_id}')]
            ]
        else:
            keyboard = []

        keyboard.append([InlineKeyboardButton(text=cls.texts['delete'], callback_data=f'delete_good_{good_id}')])
        keyboard.append([InlineKeyboardButton(text=cls.texts['back'], callback_data=data)])
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def categories(cls, callback: str, categories: list[Category], data: str):
        keyboard = []
        for category in categories:
            keyboard.append([InlineKeyboardButton(text=category.name, callback_data=f"{callback}_{category.id}")])
        keyboard.append([InlineKeyboardButton(text=cls.texts['back'], callback_data=data)])
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def subcategories(cls, callback: str, subcategories: list[Subcategory], data: str, category_id: int,
                            delete: bool = True):
        keyboard, i = [[InlineKeyboardButton(text=cls.texts['delete'],
                                             callback_data=f'delete_category_{category_id}')]], 0

        if not delete:
            keyboard = []

        for subcategory in subcategories:
            if i % 2 == 0:
                keyboard.append(
                    [InlineKeyboardButton(text=subcategory.name, callback_data=f"{callback}_{subcategory.id}")])
            else:
                keyboard[-1].append(
                    InlineKeyboardButton(text=subcategory.name, callback_data=f"{callback}_{subcategory.id}"))
            i += 1
        keyboard.append([InlineKeyboardButton(text=cls.texts['back'], callback_data=data)])
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def goods(cls, callback: str, goods: list[Good], data: str, subcategory_id: int = None,
                    category_id: int = None):
        keyboard = [[InlineKeyboardButton(text=cls.texts['delete'],
                                          callback_data=f'delete_category_{category_id}' if category_id else
                                          f"delete_subcategory_{subcategory_id}")]]
        for good in goods:
            keyboard.append(
                [InlineKeyboardButton(text=f"{good.name} ⸰ {good.price}₽",
                                      callback_data=f"{callback}_{good.id}")])

        keyboard.append([InlineKeyboardButton(text=cls.texts['back'], callback_data=data)])
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def my_shops(cls, shops: list[Shop]):
        keyboard = [
            [InlineKeyboardButton(text=cls.texts['get_shops_list_btn'], callback_data="get_shops_list")]
        ]
        for shop in shops:
            keyboard.append([InlineKeyboardButton(text=shop.username, callback_data=f"shop_{shop.id}")])
        keyboard.append([InlineKeyboardButton(text=cls.texts['back'], callback_data="constructor")])
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def shop_profile(cls, shop_id: int, shop_on: bool):
        text = cls.texts['shop_on'] if shop_on else cls.texts['shop_off']
        callback_data = f"off_{shop_id}" if shop_on else f"on_{shop_id}"
        keyboard = [
            [InlineKeyboardButton(text=text, callback_data=callback_data),
             InlineKeyboardButton(text=cls.texts['statistics'], callback_data=f"statistics_1_{shop_id}")],
            [InlineKeyboardButton(text=cls.texts['mailing'], callback_data=f"mailing_{shop_id}"),
             InlineKeyboardButton(text=cls.texts['settings'], callback_data=f"settings_{shop_id}")],
            [InlineKeyboardButton(text=cls.texts['back'], callback_data="my_shops")]
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def statistics(cls, shop_id: int, period: int):
        keyboard = [
            [InlineKeyboardButton(text=cls.texts['period_1'], callback_data=f"statistics_1_{shop_id}"),
             InlineKeyboardButton(text=cls.texts['period_2'], callback_data=f"statistics_2_{shop_id}")],
            [InlineKeyboardButton(text=cls.texts['period_3'], callback_data=f"statistics_3_{shop_id}"),
             InlineKeyboardButton(text=cls.texts['period_4'], callback_data=f"statistics_4_{shop_id}")],
            [InlineKeyboardButton(text=cls.texts['period_5'], callback_data=f"statistics_5_{shop_id}")],
            [InlineKeyboardButton(text=cls.texts['back'], callback_data=f"shop_{shop_id}")]
        ]

        if period == 1:
            keyboard[0][0].text = "✅" + cls.texts["period_1"]
        elif period == 2:
            keyboard[0][1].text = "✅" + cls.texts["period_2"]
        elif period == 3:
            keyboard[1][0].text = "✅" + cls.texts["period_3"]
        elif period == 4:
            keyboard[1][1].text = "✅" + cls.texts["period_4"]
        elif period == 5:
            keyboard[2][0].text = "✅" + cls.texts["period_5"]

        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def settings_list(cls, shop_id: int, notification: bool, count_users: int, channel: str = None):
        status = "Вкл" if notification else "Выкл"
        channel_btn = cls.texts['link_btn'] if channel is None else cls.texts['unlink_btn']
        keyboard = [
            [InlineKeyboardButton(text=cls.texts['notification_btn'].format(status),
                                  callback_data=f"notification_{shop_id}")],
            [InlineKeyboardButton(text=cls.texts['users_btn'].format(count_users), callback_data=f"users_{shop_id}")],
            [InlineKeyboardButton(text=cls.texts['change_extra_charge_btn'], callback_data=f"extra_charge_{shop_id}")],
            [InlineKeyboardButton(text=channel_btn, callback_data=f"link_{shop_id}")],
            [InlineKeyboardButton(text=cls.texts['change_token_btn'], callback_data=f"change_token_{shop_id}")],
            [InlineKeyboardButton(text=cls.texts['delete_shop_btn'], callback_data=f"delete_shop_{shop_id}")],
            [InlineKeyboardButton(text=cls.texts['back'], callback_data=f"shop_{shop_id}")]
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def extra_charge(cls, shop_id: int):
        keyboard = []
        percent = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 200, 300, 400, 500]
        for i in range(len(percent)):
            if i % 4 == 0:
                keyboard.append(
                    [InlineKeyboardButton(text=f"{percent[i]}%", callback_data=f"percent_{percent[i]}_{shop_id}")])
            else:
                keyboard[-1].append(
                    InlineKeyboardButton(text=f"{percent[i]}%", callback_data=f"percent_{percent[i]}_{shop_id}"))
        keyboard.append([InlineKeyboardButton(text=cls.texts['back'], callback_data=f"settings_{shop_id}")])
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def admin_statistics(cls, period: int = 1):
        keyboard = [
            [InlineKeyboardButton(text=cls.texts['period_1'], callback_data=f"adminStatistics_1"),
             InlineKeyboardButton(text=cls.texts['period_2'], callback_data=f"adminStatistics_2")],
            [InlineKeyboardButton(text=cls.texts['period_3'], callback_data=f"adminStatistics_3"),
             InlineKeyboardButton(text=cls.texts['period_4'], callback_data=f"adminStatistics_4")],
            [InlineKeyboardButton(text=cls.texts['period_5'], callback_data=f"adminStatistics_5")],
            [InlineKeyboardButton(text=cls.texts['back'], callback_data=f"admin_statistics_shops")]
        ]

        if period == 1:
            keyboard[0][0].text = "✅" + cls.texts["period_1"]
        elif period == 2:
            keyboard[0][1].text = "✅" + cls.texts["period_2"]
        elif period == 3:
            keyboard[1][0].text = "✅" + cls.texts["period_3"]
        elif period == 4:
            keyboard[1][1].text = "✅" + cls.texts["period_4"]
        elif period == 5:
            keyboard[2][0].text = "✅" + cls.texts["period_5"]

        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def all_statistics(cls, period: int):
        keyboard = [
            [InlineKeyboardButton(text=cls.texts['period_1'], callback_data=f"allStatistics_1"),
             InlineKeyboardButton(text=cls.texts['period_2'], callback_data=f"allStatistics_2")],
            [InlineKeyboardButton(text=cls.texts['period_3'], callback_data=f"allStatistics_3"),
             InlineKeyboardButton(text=cls.texts['period_4'], callback_data=f"allStatistics_4")],
            [InlineKeyboardButton(text=cls.texts['period_5'], callback_data=f"allStatistics_5")],
            [InlineKeyboardButton(text=cls.texts['back'], callback_data=f"constructor")]
        ]

        if period == 1:
            keyboard[0][0].text = "✅" + cls.texts["period_1"]
        elif period == 2:
            keyboard[0][1].text = "✅" + cls.texts["period_2"]
        elif period == 3:
            keyboard[1][0].text = "✅" + cls.texts["period_3"]
        elif period == 4:
            keyboard[1][1].text = "✅" + cls.texts["period_4"]
        elif period == 5:
            keyboard[2][0].text = "✅" + cls.texts["period_5"]

        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def users_db(cls, shop_id: int):
        keyboard = [
            [InlineKeyboardButton(text=cls.texts['get_users_btn'], callback_data=f"get_users_{shop_id}")],
            [InlineKeyboardButton(text=cls.texts['back'], callback_data=f"settings_{shop_id}")],
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def solution_admin_funds(cls, funds_id: int):
        keyboard = [
            [InlineKeyboardButton(text=cls.texts['successful_payments'],
                                  callback_data=f"successful_payments_{funds_id}"),
             InlineKeyboardButton(text=cls.texts['bad_payments'], callback_data=f"bad_payments_{funds_id}")]
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def subscribe(cls, channel: str):
        keyboard = [
            [InlineKeyboardButton(text=cls.texts['subscribe'], url=f"{channel}")],
            [InlineKeyboardButton(text=cls.texts['check'], callback_data="start")],
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def subpartner(cls, is_partner: bool, user_id: int = None):
        if is_partner:
            keyboard = [
                [InlineKeyboardButton(text=cls.texts['share_frens'],
                                      url=f"https://t.me/share/url?url=https://t.me/{MAIN_BOT_LINK}?start={user_id}")]
            ]
        else:
            keyboard = [
                [InlineKeyboardButton(text=cls.texts['submit_app_btn'], callback_data="submit_app")],
            ]

        keyboard.append([InlineKeyboardButton(text=cls.texts['back'], callback_data="constructor")])
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def solution_admin_subpartner(cls, request_id: int, username: str):
        keyboard = [
            [InlineKeyboardButton(text=cls.texts['successful_payments'],
                                  callback_data=f"successful_request_{request_id}"),
             InlineKeyboardButton(text=cls.texts['bad_payments'], callback_data=f"bad_request_{request_id}")],
            [InlineKeyboardButton(text=cls.texts['link_with_user'], url=f"t.me/{username}")]
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def mailing_list(cls, shop_id: int, my_mail: MyMail):
        keyboard = [
            [InlineKeyboardButton(text=cls.texts['add_mail_btn'], callback_data=f"add_mail")],
        ]

        for i in range(my_mail.cur_page * 5, my_mail.cur_page * 5 + 5):
            try:
                if my_mail.mails[i].status == "wait":
                    emoji = "🟠"
                elif my_mail.mails[i].status == "done":
                    emoji = "🟢"
                else:
                    emoji = "🔴"

                try:
                    keyboard.append([InlineKeyboardButton(
                        text=cls.texts["schedule_mail_btn"].format(emoji, my_mail.mails[i].id,
                                                                   my_mail.mails[i].real_date.strftime(
                                                                       "%d.%m.%Y %H:%M")),
                        callback_data=f"mail_{my_mail.mails[i].id}")])
                except AttributeError:
                    keyboard.append([InlineKeyboardButton(
                        text=cls.texts["schedule_mail_btn"].format(emoji, my_mail.mails[i].id,
                                                                   my_mail.mails[i].wait_date.strftime(
                                                                       "%d.%m.%Y %H:%M")),
                        callback_data=f"mail_{my_mail.mails[i].id}")])
            except IndexError:
                pass

        if my_mail.mails:
            keyboard.append([InlineKeyboardButton(text=cls.texts["<"], callback_data="back_page_mail"),
                             InlineKeyboardButton(
                                 text=cls.texts["page"].format(my_mail.cur_page + 1, my_mail.all_pages),
                                 callback_data="just_page"),
                             InlineKeyboardButton(text=cls.texts['>'], callback_data="next_page_mail")])

        keyboard.append([InlineKeyboardButton(text=cls.texts['back'], callback_data=f"shop_{shop_id}")])
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def all_mailing_list(cls, my_mail: MyMail):
        keyboard = [
            [InlineKeyboardButton(text=cls.texts['add_mail_btn'], callback_data=f"add_all_mail")],
        ]

        for i in range(my_mail.cur_page * 5, my_mail.cur_page * 5 + 5):
            try:
                if my_mail.mails[i].status == "wait":
                    emoji = "🟠"
                elif my_mail.mails[i].status == "done":
                    emoji = "🟢"
                else:
                    emoji = "🔴"

                try:
                    keyboard.append([InlineKeyboardButton(
                        text=cls.texts["schedule_mail_btn"].format(emoji, my_mail.mails[i].id,
                                                                   my_mail.mails[i].real_date.strftime(
                                                                       "%d.%m.%Y %H:%M")),
                        callback_data=f"all_mail_{my_mail.mails[i].id}")])
                except AttributeError:
                    keyboard.append([InlineKeyboardButton(
                        text=cls.texts["schedule_mail_btn"].format(emoji, my_mail.mails[i].id,
                                                                   my_mail.mails[i].wait_date.strftime(
                                                                       "%d.%m.%Y %H:%M")),
                        callback_data=f"all_mail_{my_mail.mails[i].id}")])
            except IndexError:
                pass

        if my_mail.mails:
            keyboard.append([InlineKeyboardButton(text=cls.texts["<"], callback_data="back_page_all_mail"),
                             InlineKeyboardButton(
                                 text=cls.texts["page"].format(my_mail.cur_page + 1, my_mail.all_pages),
                                 callback_data="just_page"),
                             InlineKeyboardButton(text=cls.texts['>'], callback_data="next_page_all_mail")])

        keyboard.append([InlineKeyboardButton(text=cls.texts['back'], callback_data="constructor")])
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def add_mail_kb(cls, shop_id: int, date: str = None):
        date = date if date else "Сейчас"
        keyboard = [
            [InlineKeyboardButton(text=cls.texts['date_btn'].format(date), callback_data=f"date")],
            [InlineKeyboardButton(text=cls.texts['add_btn'], callback_data=f"add_btn")],
            [InlineKeyboardButton(text=cls.texts['save_btn'], callback_data=f"save_btn")],
            [InlineKeyboardButton(text=cls.texts['cancel'], callback_data=f"shop_{shop_id}")]
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def add_all_mail_kb(cls, date: str = None):
        date = date if date else "Сейчас"
        keyboard = [
            [InlineKeyboardButton(text=cls.texts['date_btn'].format(date), callback_data=f"all_date")],
            [InlineKeyboardButton(text=cls.texts['add_btn'], callback_data=f"all_add_btn")],
            [InlineKeyboardButton(text=cls.texts['save_btn'], callback_data=f"all_save_btn")],
            [InlineKeyboardButton(text=cls.texts['cancel'], callback_data=f"constructor")]
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def mail_profile_kb(cls, deleted: bool):
        if not deleted:
            keyboard = [
                [InlineKeyboardButton(text=cls.texts['delete_mail'], callback_data=f"delete_mail")],
            ]
        else:
            keyboard = []

        keyboard.append([InlineKeyboardButton(text=cls.texts['view_mail'], callback_data=f"view_mail")])
        keyboard.append([InlineKeyboardButton(text=cls.texts['back'], callback_data=f"mailing_")])

        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def all_mail_profile_kb(cls, deleted: bool):
        if not deleted:
            keyboard = [
                [InlineKeyboardButton(text=cls.texts['delete_mail'], callback_data=f"all_delete_mail")],
            ]
        else:
            keyboard = []

        keyboard.append([InlineKeyboardButton(text=cls.texts['view_mail'], callback_data=f"all_view_mail")])
        keyboard.append([InlineKeyboardButton(text=cls.texts['back'], callback_data=f"all_mailing_list")])

        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def generate_keyboard(cls, text: str | None, url_l: str | None):
        if text and url_l:
            keyboard = [
                [InlineKeyboardButton(text=text, url=url_l)]
            ]
            return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def statistics_menu(cls):
        keyboard = [
            [InlineKeyboardButton(text=cls.texts['statistics_users'], callback_data=f"admin_statistics_users")],
            [InlineKeyboardButton(text=cls.texts['statistics_shops'], callback_data=f"admin_statistics_shops")],
            [InlineKeyboardButton(text=cls.texts['all_statistics_time_line'],
                                  callback_data=f"admin_all_statistics_time_line")],
            [InlineKeyboardButton(text=cls.texts['statistics_time_line'],
                                  callback_data=f"admin_statistics_time_line")],
            [InlineKeyboardButton(text=cls.texts['back'], callback_data=f"admin_panel")]
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)
