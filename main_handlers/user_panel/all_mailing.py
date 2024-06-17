import re

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, FSInputFile

from config.config import TZ, schedular
from database.schemas.Mail import Mail
from database.schemas.Shop import Shop
from utils import load_texts, MyMail
from database.commands import Database
from keyboards import InlineKeyboardMain

from dataclasses import dataclass
from datetime import datetime, timedelta
from states.main_bot import AddAllMail
from utils.schedular import send_mail

statuses = {
    "done": "Выполнена",
    "wait": "Ожидает запуска",
    "cancel": "Отменена"
}


@dataclass
class MailData:
    text: str = None
    photo: str = None
    keyboard: str = None
    date: datetime = None


async def all_mailing_list(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()

    mails = await Database.Mail.get_all_user_mails(callback.message.chat.id)
    all_pages = int(len(mails) / 5) + (len(mails) % 5 != 0) if mails else 1
    my_mail = MyMail(mails=mails, all_pages=all_pages)
    await state.update_data(my_mail=my_mail)

    await callback.message.delete()
    return await callback.message.answer(text=texts['all_mailing_list'],
                                         reply_markup=await InlineKeyboardMain.all_mailing_list(my_mail))


async def all_change_page(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    my_mail: MyMail = data.get("my_mail")

    action = callback.data.split("_")[0]

    if action == "next":
        if my_mail.cur_page + 1 < my_mail.all_pages:
            my_mail.cur_page += 1
        else:
            return callback.answer(text=texts['last_page'], show_alert=True)
    else:
        if my_mail.cur_page > 0:
            my_mail.cur_page -= 1
        else:
            return callback.answer(text=texts['first_page'], show_alert=True)

    await state.update_data(my_mail=my_mail)
    await callback.message.delete()
    return await callback.message.answer(text=texts['all_mailing_list'],
                                         reply_markup=await InlineKeyboardMain.all_mailing_list(my_mail))


async def all_view_adding_mail(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    mail: MailData = data.get("mail")

    await state.set_state(None)
    await callback.message.delete()

    button = f"\n\n{mail.keyboard}" if mail.keyboard else ""
    date = mail.date.strftime("%d.%m.%Y %H:%M") if mail.date else None
    if mail.photo:
        return await callback.message.answer_photo(photo=mail.photo, caption=mail.text + button,
                                                   reply_markup=await InlineKeyboardMain.add_all_mail_kb(date),
                                                   disable_web_page_preview=True)
    else:
        return await callback.message.answer(text=mail.text + button,
                                             reply_markup=await InlineKeyboardMain.add_all_mail_kb(date),
                                             disable_web_page_preview=True)


async def all_add_mail(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()

    await state.set_state(AddAllMail.text)
    await callback.message.delete()
    return await callback.message.answer(text=texts['all_add_mail'])


async def all_get_text_photo(message: Message, state: FSMContext):
    await state.set_state(None)

    if message.photo:
        photo_id = message.photo[-1].file_id
        mail = MailData(text=message.html_text, photo=message.photo[-1].file_id)
        await state.update_data(mail=mail)
        await message.answer_photo(photo=photo_id, caption=message.html_text,
                                   reply_markup=await InlineKeyboardMain.add_all_mail_kb(),
                                   disable_web_page_preview=True)
    else:
        mail = MailData(text=message.html_text)
        await message.answer(text=message.html_text, reply_markup=await InlineKeyboardMain.add_all_mail_kb(),
                             disable_web_page_preview=True)

    return await state.update_data(mail=mail)


async def all_add_date(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    await state.set_state(AddAllMail.date)
    await callback.message.delete()
    return await callback.message.answer(text=texts['add_date'].format(datetime.now(tz=TZ).strftime("%d.%m.%Y %H:%M")),
                                         reply_markup=await InlineKeyboardMain.back("all_view_adding_mail"))


async def all_get_date(message: Message, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    mail: MailData = data.get("mail")

    date = datetime.strptime(message.text, "%d.%m.%Y %H:%M")
    if not date or date.timestamp() < (datetime.now(tz=TZ) + timedelta(minutes=5)).timestamp():
        return await message.answer(text=texts['fail_date'])

    mail.date = date
    await state.update_data(mail=mail)
    await state.set_state(None)

    button = f"\n\n{mail.keyboard}" if mail.keyboard else ""
    if mail.photo:
        return await message.answer_photo(photo=mail.photo, caption=mail.text + button,
                                          reply_markup=await InlineKeyboardMain.add_all_mail_kb(date.strftime(
                                              "%d.%m.%Y %H:%M")),
                                          disable_web_page_preview=True)
    else:
        return await message.answer(text=mail.text + button,
                                    reply_markup=await InlineKeyboardMain.add_all_mail_kb(
                                        date.strftime("%d.%m.%Y %H:%M")),
                                    disable_web_page_preview=True)


async def all_add_btn(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    mail: MailData = (await state.get_data()).get("mail")

    if mail.keyboard:
        return await callback.answer(text=texts['exists_btn'], show_alert=True)

    await state.set_state(AddAllMail.button)
    await callback.message.delete()
    return await callback.message.answer(text=texts['add_btn_text'],
                                         reply_markup=await InlineKeyboardMain.back("all_view_adding_mail"))


async def all_get_btn(message: Message, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    mail: MailData = data.get("mail")

    btn = re.match("\[.+ - \S+]", message.text)
    if not btn:
        return await message.answer(text=texts['fail_btn'])

    mail.keyboard = btn.string
    await state.update_data(mail=mail)
    await state.set_state(None)

    button = f"\n\n{mail.keyboard}" if mail.keyboard else ""
    date = mail.date.strftime("%d.%m.%Y %H:%M") if mail.date else None
    if mail.photo:
        return await message.answer_photo(photo=mail.photo, caption=mail.text + button,
                                          reply_markup=await InlineKeyboardMain.add_all_mail_kb(date),
                                          disable_web_page_preview=True)
    else:
        return await message.answer(text=mail.text + button,
                                    reply_markup=await InlineKeyboardMain.add_all_mail_kb(date),
                                    disable_web_page_preview=True)


async def all_save_mail(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    mail: MailData = data.get("mail")
    user = await Database.MainBot.get_user(callback.message.chat.id)

    mail.date = mail.date if mail.date else (datetime.now() + timedelta(seconds=10))
    if mail.photo:
        await callback.bot.download(mail.photo, f"./photos/mailing/{mail.photo}.jpg")
    await Database.Mail.insert_mail(callback.message.chat.id, user.shops, mail)
    last_mail = await Database.Mail.get_last_mail()

    schedular.add_job(func=send_mail, trigger="date", id=f"mail_{last_mail.id}", args=(last_mail.id,),
                      next_run_time=last_mail.wait_date)

    await callback.message.delete()
    return callback.message.answer(text=texts['all_save_mail'],
                                   reply_markup=await InlineKeyboardMain.back("all_mailing_list"))


async def all_view_profile_mail(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    mail = await Database.Mail.get_mail(int(callback.data.split("_")[2]))

    await state.update_data(mail=mail)

    shop = "Все ваши магазины" if len(mail.shop_id) != 1 else (
        await Database.MainBot.get_shop(mail.shop_id[0])).username
    date = mail.real_date.strftime("%d.%m.%Y %H:%M") if mail.real_date else mail.wait_date.strftime("%d.%m.%Y %H:%M")
    await callback.message.delete()
    return await callback.message.answer(text=texts['mail_profile'].format(id=mail.id,
                                                                           shop=shop,
                                                                           status=statuses[mail.status],
                                                                           all=mail.all_send,
                                                                           send=mail.successful_send,
                                                                           fail=mail.failed_send,
                                                                           date=date),
                                         reply_markup=await InlineKeyboardMain.all_mail_profile_kb(
                                             mail.status == "cancel" or mail.status == "done"))


async def all_view_mail(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    mail: Mail = data.get("mail")

    await callback.message.delete()
    if mail.photo:
        return await callback.message.answer_photo(photo=FSInputFile(path=f"./photos/mailing/{mail.photo}.jpg",
                                                                     filename="mail.jpg"),
                                                   caption=mail.text + (
                                                       f"\n\n{mail.keyboard}" if mail.keyboard else ""),
                                                   reply_markup=await InlineKeyboardMain.back(f"all_mail_{mail.id}"))

    return await callback.message.answer(text=mail.text + (f"\n\n{mail.keyboard}" if mail.keyboard else ""),
                                         reply_markup=await InlineKeyboardMain.back(f"all_mail_{mail.id}"))


async def all_delete_mail(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    mail: Mail = data.get("mail")

    date = mail.real_date.strftime("%d.%m.%Y %H:%M") if mail.real_date else mail.wait_date.strftime("%d.%m.%Y %H:%M")
    shop = "Все ваши магазины" if len(mail.shop_id) != 1 else (
        await Database.MainBot.get_shop(mail.shop_id[0])).username

    schedular.remove_job(f"mail_{mail.id}", "default")

    await Database.Mail.update_status(mail.id, "cancel")
    await callback.message.delete()
    return await callback.message.answer(text=texts['mail_profile'].format(id=mail.id,
                                                                           shop=shop,
                                                                           status=statuses[mail.status],
                                                                           all=mail.all_send,
                                                                           send=mail.successful_send,
                                                                           fail=mail.failed_send,
                                                                           date=date),
                                         reply_markup=await InlineKeyboardMain.all_mail_profile_kb(
                                             mail.status == "cancel" or mail.status == "done"))
