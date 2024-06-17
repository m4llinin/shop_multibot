from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.types import FSInputFile
from datetime import datetime

from config.config import session, TZ
from database.commands import Database
from database.schemas.Mail import Mail
from keyboards import InlineKeyboardMain


async def send_mail(mail_id: int):
    mail: Mail = await Database.Mail.get_mail(mail_id)

    text, url = None, None
    if mail.keyboard:
        text, url = mail.keyboard[1:-1].split("-")

    send, fail = 0, 0
    for shop_id in mail.shop_id:
        shop = await Database.MainBot.get_shop(shop_id)
        users_of_shop = await Database.MainBot.get_all_users_of_shop(shop.id)
        bot = Bot(token=shop.token, session=session)
        for user in users_of_shop:
            try:
                if mail.photo:
                    await bot.send_photo(chat_id=user.id,
                                         photo=FSInputFile(path=f"./photos/mailing/{mail.photo}.jpg",
                                                           filename="mail.jpg"),
                                         caption=mail.text,
                                         reply_markup=await InlineKeyboardMain.generate_keyboard(text, url[1:]),
                                         parse_mode=ParseMode.HTML)
                else:
                    await bot.send_message(chat_id=user.id,
                                           text=mail.text,
                                           reply_markup=await InlineKeyboardMain.generate_keyboard(text, url),
                                           parse_mode=ParseMode.HTML)
                send += 1
            except:
                fail += 1

    return await Database.Mail.update_status(mail.id, "done", send, fail, send + fail, datetime.now())
