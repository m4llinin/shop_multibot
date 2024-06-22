import re
from datetime import datetime

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config.config import TZ
from utils import load_texts
from keyboards import InlineKeyboardMain
from database.commands import Database

from states.main_bot import Statistics


async def get_name_shop(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    texts = await load_texts()

    await state.set_state(Statistics.shop_period)
    await callback.message.delete()
    await callback.message.answer(text=texts['input_shop'],
                                  reply_markup=await InlineKeyboardMain.back("admin_statistics"))


async def statistics_time_line(message: Message, state: FSMContext):
    texts = await load_texts()

    username = message.text
    if username[0] == "@":
        username = message.text[1:]

    shop = await Database.MainBot.get_shop(username)
    if not shop:
        return await message.answer(text=texts['shop_not_found'],
                                    reply_markup=await InlineKeyboardMain.back("admin_statistics"))

    await state.update_data(shop_username=username)

    now = datetime.now(tz=TZ).strftime("%d.%m.%Y")
    await state.set_state(Statistics.period)
    await message.answer(text=texts['input_period'].format(date=now),
                         reply_markup=await InlineKeyboardMain.back("admin_statistics"))


async def get_period(message: Message, state: FSMContext):
    texts = await load_texts()

    if not re.match("\d{2}\.\d{2}\.\d{4}-\d{2}\.\d{2}\.\d{4}", message.text):
        return await message.answer(text=texts['invalid_period'],
                                    reply_markup=await InlineKeyboardMain.back("admin_statistics"))

    try:
        start, end = datetime.strptime(message.text.split("-")[0] + " 00:00", "%d.%m.%Y %H:%M"), datetime.strptime(
            message.text.split("-")[1] + " 23:59", "%d.%m.%Y %H:%M")
    except:
        return await message.answer(text=texts['invalid_time'],
                                    reply_markup=await InlineKeyboardMain.back("admin_statistics"))

    await state.set_state(None)
    shop_username = (await state.get_data()).get("shop_username")

    shop = await Database.MainBot.get_shop(shop_username)
    profit = await Database.MainBot.get_profit(shop.id, start, end)
    sales = await Database.MainBot.get_sales(shop.id, start, end)
    users = await Database.MainBot.get_users_shop(shop.id, start, end)

    await message.answer(text=texts['periodStatistics'].format(profit=profit,
                                                               sales=sales,
                                                               users=users,
                                                               date=message.text,
                                                               shop=shop.username),
                         reply_markup=await InlineKeyboardMain.back("admin_statistics_time_line"))
