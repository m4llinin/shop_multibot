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
from states.main_bot import AddAdminMail
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
    loop: str = None


async def admin_mailing_list(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    mails = await Database.Mail.get_admin_mails(callback.message.chat.id)
    all_pages = int(len(mails) / 5) + (len(mails) % 5 != 0) if mails else 1
    my_mail = MyMail(mails=mails, all_pages=all_pages)
    await state.update_data(my_mail=my_mail)

    await callback.message.delete()
    return await callback.message.answer(text=texts['all_mailing_list'],
                                         reply_markup=await InlineKeyboardMain.admin_mailing_list(my_mail))


async def admin_change_page(callback: CallbackQuery, state: FSMContext):
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
                                         reply_markup=await InlineKeyboardMain.admin_mailing_list(my_mail))


async def admin_view_adding_mail(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    mail: MailData = data.get("mail")

    await state.set_state(None)
    await callback.message.delete()

    button = f"\n\n{mail.keyboard}" if mail.keyboard else ""
    date = mail.date.strftime("%d.%m.%Y %H:%M") if mail.date else None
    if mail.photo:
        return await callback.message.answer_photo(photo=mail.photo, caption=mail.text + button,
                                                   reply_markup=await InlineKeyboardMain.add_admin_mail_kb(date,
                                                                                                           mail.loop),
                                                   disable_web_page_preview=True)
    else:
        return await callback.message.answer(text=mail.text + button,
                                             reply_markup=await InlineKeyboardMain.add_admin_mail_kb(date, mail.loop),
                                             disable_web_page_preview=True)


async def admin_add_mail(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()

    await state.set_state(AddAdminMail.text)
    await callback.message.delete()
    return await callback.message.answer(text=texts['all_add_mail'])


async def admin_get_text_photo(message: Message, state: FSMContext):
    await state.set_state(None)

    if message.photo:
        photo_id = message.photo[-1].file_id
        mail = MailData(text=message.html_text, photo=message.photo[-1].file_id)
        await state.update_data(mail=mail)
        await message.answer_photo(photo=photo_id, caption=message.html_text,
                                   reply_markup=await InlineKeyboardMain.add_admin_mail_kb(),
                                   disable_web_page_preview=True)
    else:
        mail = MailData(text=message.html_text)
        await message.answer(text=message.html_text, reply_markup=await InlineKeyboardMain.add_admin_mail_kb(),
                             disable_web_page_preview=True)

    return await state.update_data(mail=mail)


async def admin_add_date(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    await state.set_state(AddAdminMail.date)
    await callback.message.delete()
    return await callback.message.answer(text=texts['add_date'].format(datetime.now(tz=TZ).strftime("%d.%m.%Y %H:%M")),
                                         reply_markup=await InlineKeyboardMain.back("admin_view_adding_mail"))


async def admin_get_date(message: Message, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    mail: MailData = data.get("mail")

    date = datetime.strptime(message.text, "%d.%m.%Y %H:%M")
    if not date or date.timestamp() < (datetime.now(tz=TZ) + timedelta(minutes=3)).timestamp():
        return await message.answer(text=texts['fail_date'])

    mail.date = date
    await state.update_data(mail=mail)
    await state.set_state(None)

    button = f"\n\n{mail.keyboard}" if mail.keyboard else ""
    if mail.photo:
        return await message.answer_photo(photo=mail.photo, caption=mail.text + button,
                                          reply_markup=await InlineKeyboardMain.add_admin_mail_kb(date.strftime(
                                              "%d.%m.%Y %H:%M"), mail.loop),
                                          disable_web_page_preview=True)
    else:
        return await message.answer(text=mail.text + button,
                                    reply_markup=await InlineKeyboardMain.add_admin_mail_kb(
                                        date.strftime("%d.%m.%Y %H:%M"), mail.loop),
                                    disable_web_page_preview=True)


async def admin_add_btn(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    mail: MailData = (await state.get_data()).get("mail")

    if mail.keyboard:
        return await callback.answer(text=texts['exists_btn'], show_alert=True)

    await state.set_state(AddAdminMail.button)
    await callback.message.delete()
    return await callback.message.answer(text=texts['add_btn_text'],
                                         reply_markup=await InlineKeyboardMain.back("admin_view_adding_mail"))


async def admin_get_btn(message: Message, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    mail: MailData = data.get("mail")

    btn = re.match(r"\[.+ - \S+]", message.text)
    if not btn:
        return await message.answer(text=texts['fail_btn'])

    mail.keyboard = btn.string
    await state.update_data(mail=mail)
    await state.set_state(None)

    button = f"\n\n{mail.keyboard}" if mail.keyboard else ""
    date = mail.date.strftime("%d.%m.%Y %H:%M") if mail.date else None
    if mail.photo:
        return await message.answer_photo(photo=mail.photo, caption=mail.text + button,
                                          reply_markup=await InlineKeyboardMain.add_admin_mail_kb(date, mail.loop),
                                          disable_web_page_preview=True)
    else:
        return await message.answer(text=mail.text + button,
                                    reply_markup=await InlineKeyboardMain.add_admin_mail_kb(date, mail.loop),
                                    disable_web_page_preview=True)


async def admin_add_loop(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    await state.set_state(AddAdminMail.loop)
    await callback.message.delete()
    return await callback.message.answer(text=texts['add_loop'],
                                         reply_markup=await InlineKeyboardMain.back("admin_view_adding_mail"))


async def admin_get_loop(message: Message, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    mail: MailData = data.get("mail")

    loop = re.match(r"\d+:\d+", message.text)
    if not loop:
        return await message.answer(text=texts['fail_loop'])

    try:
        hour, minute = list(map(int, loop.string.split(":")))
        # if not (1 <= minute <= 59):
        #     raise ValueError
    except ValueError:
        return await message.answer(text=texts['fail_loop'])

    mail.loop = loop.string
    await state.update_data(mail=mail)
    await state.set_state(None)

    button = f"\n\n{mail.keyboard}" if mail.keyboard else ""
    date = mail.date.strftime("%d.%m.%Y %H:%M") if mail.date else None
    if mail.photo:
        return await message.answer_photo(photo=mail.photo, caption=mail.text + button,
                                          reply_markup=await InlineKeyboardMain.add_admin_mail_kb(date, mail.loop),
                                          disable_web_page_preview=True)
    else:
        return await message.answer(text=mail.text + button,
                                    reply_markup=await InlineKeyboardMain.add_admin_mail_kb(date, mail.loop),
                                    disable_web_page_preview=True)


async def admin_save_mail(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    mail: MailData = data.get("mail")

    mail.date = mail.date if mail.date else (datetime.now() + timedelta(seconds=10))
    if mail.photo:
        await callback.bot.download(mail.photo, f"./photos/mailing/{mail.photo}.jpg")
    shops = await Database.MainBot.get_all_shops()
    shop_ids = [shop.id for shop in shops]

    await Database.Mail.insert_mail(callback.message.chat.id, shop_ids, mail)
    last_mail = await Database.Mail.get_last_mail()

    schedular.add_job(func=send_mail, trigger="date", id=f"mail_{last_mail.id}", args=(last_mail.id,),
                      next_run_time=last_mail.wait_date)
    await callback.message.delete()
    return callback.message.answer(text=texts['all_save_mail'],
                                   reply_markup=await InlineKeyboardMain.back("admin_mailing_list"))


async def admin_view_profile_mail(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    mail = await Database.Mail.get_mail(int(callback.data.split("_")[2]))

    await state.update_data(mail=mail)

    date = mail.real_date.strftime("%d.%m.%Y %H:%M") if mail.real_date else mail.wait_date.strftime("%d.%m.%Y %H:%M")
    await callback.message.delete()
    return await callback.message.answer(text=texts['admin_mail_profile'].format(id=mail.id,
                                                                                 status=statuses[mail.status],
                                                                                 all=mail.all_send,
                                                                                 send=mail.successful_send,
                                                                                 fail=mail.failed_send,
                                                                                 date=date),
                                         reply_markup=await InlineKeyboardMain.admin_mail_profile_kb(
                                             mail.status == "cancel" or mail.status == "done"))


async def admin_view_mail(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    mail: Mail = data.get("mail")

    await callback.message.delete()
    if mail.photo:
        return await callback.message.answer_photo(photo=FSInputFile(path=f"./photos/mailing/{mail.photo}.jpg",
                                                                     filename="mail.jpg"),
                                                   caption=mail.text + (
                                                       f"\n\n{mail.keyboard}" if mail.keyboard else ""),
                                                   reply_markup=await InlineKeyboardMain.back(f"admin_mail_{mail.id}"))

    return await callback.message.answer(text=mail.text + (f"\n\n{mail.keyboard}" if mail.keyboard else ""),
                                         reply_markup=await InlineKeyboardMain.back(f"admin_mail_{mail.id}"))


async def admin_delete_mail(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    mail: Mail = data.get("mail")

    date = mail.real_date.strftime("%d.%m.%Y %H:%M") if mail.real_date else mail.wait_date.strftime("%d.%m.%Y %H:%M")

    schedular.remove_job(f"mail_{mail.id}", "default")

    await Database.Mail.update_status(mail.id, "cancel")
    mail.status = "cancel"
    await state.update_data(mail=mail)
    await callback.message.delete()
    return await callback.message.answer(text=texts['admin_mail_profile'].format(id=mail.id,
                                                                                 status=statuses[mail.status],
                                                                                 all=mail.all_send,
                                                                                 send=mail.successful_send,
                                                                                 fail=mail.failed_send,
                                                                                 date=date),
                                         reply_markup=await InlineKeyboardMain.admin_mail_profile_kb(
                                             mail.status == "cancel" or mail.status == "done"))


async def edit_mail_text(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    mail: Mail = data.get("mail")

    await state.set_state(AddAdminMail.edit_text)
    await callback.message.delete()
    await callback.message.answer(text=texts['edit_mail_text'],
                                  reply_markup=await InlineKeyboardMain.back(f"admin_mail_{mail.id}"))


async def get_edit_mail_text(message: Message, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    mail: Mail = data.get("mail")

    await state.set_state(None)
    await Database.Mail.edit_text_mail(mail.id, message.html_text)
    await message.answer(text=texts['successful_edit'],
                         reply_markup=await InlineKeyboardMain.ready(f"admin_mail_{mail.id}"))


async def edit_mail_photo(callback: CallbackQuery, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    mail: Mail = data.get("mail")

    await state.set_state(AddAdminMail.edit_photo)
    await callback.message.delete()
    await callback.message.answer(text=texts['edit_mail_photo'],
                                  reply_markup=await InlineKeyboardMain.back(f"admin_mail_{mail.id}"))


async def get_edit_mail_photo(message: Message, state: FSMContext):
    texts = await load_texts()
    data = await state.get_data()
    mail: Mail = data.get("mail")

    await state.set_state(None)
    await message.bot.download(message.photo[-1].file_id, f"./photos/mailing/{message.photo[-1].file_id}.jpg")
    await Database.Mail.edit_photo_mail(mail.id, message.photo[-1].file_id)
    await message.answer(text=texts['successful_edit'],
                         reply_markup=await InlineKeyboardMain.ready(f"admin_mail_{mail.id}"))
