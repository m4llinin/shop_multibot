import logging
from dataclasses import dataclass

from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.types import FSInputFile
from datetime import datetime, timedelta

from config.config import session, TZ, schedular
from database.commands import Database
from database.schemas.Mail import Mail
from keyboards import InlineKeyboardMain

logger = logging.getLogger(__name__)


@dataclass
class MailData:
    text: str = None
    photo: str = None
    keyboard: str = None
    date: datetime = None
    loop: str = None


async def send_mail(mail_id: int):
    mail: Mail = await Database.Mail.get_mail(mail_id)

    text, url = None, None
    if mail.keyboard:
        text, url = mail.keyboard[1:-1].split("-")

    if url:
        url = url[1:]

    send, fail = 0, 0

    try:
        for shop_id in mail.shop_id:
            shop = await Database.MainBot.get_shop(shop_id)

            if shop is not None:
                users_of_shop = await Database.MainBot.get_all_users_of_shop(shop.id)
                bot = Bot(token=shop.token, session=session)

                new_url = url
                if new_url and "{}" in url:
                    new_url = url.format(shop.username)

                for user in users_of_shop:
                    try:
                        if mail.photo:
                            await bot.send_photo(chat_id=user.id,
                                                 photo=FSInputFile(path=f"./photos/mailing/{mail.photo}.jpg",
                                                                   filename="mail.jpg"),
                                                 caption=mail.text,
                                                 reply_markup=await InlineKeyboardMain.generate_keyboard(text, new_url),
                                                 parse_mode=ParseMode.HTML)
                        else:
                            await bot.send_message(chat_id=user.id,
                                                   text=mail.text,
                                                   reply_markup=await InlineKeyboardMain.generate_keyboard(text, new_url),
                                                   parse_mode=ParseMode.HTML)
                        send += 1
                    except Exception as e:
                        fail += 1
    except Exception as e:
        logger.error(e)

    await Database.Mail.update_status(mail.id, "done", send, fail, send + fail, datetime.now())

    if mail.loop:
        hours, minutes = list(map(int, mail.loop.split(":")))
        new_mail = MailData(mail.text, mail.photo, mail.keyboard,
                            mail.wait_date + timedelta(hours=hours, minutes=minutes), mail.loop)
        shops = await Database.MainBot.get_all_shops()

        shop_ids = []
        for shop in shops:
            try:
                shop_ids.append(shop.id)
            except Exception as e:
                logger.error(e)

        await Database.Mail.insert_mail(mail.user_id, shop_ids, new_mail)
        last_mail = await Database.Mail.get_last_mail()
        schedular.add_job(func=send_mail, trigger="date", id=f"mail_{last_mail.id}", args=(last_mail.id,),
                          next_run_time=last_mail.wait_date)
