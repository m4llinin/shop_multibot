import re
from datetime import datetime

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config.config import TZ
from utils import load_texts
from keyboards import InlineKeyboardMain
from database.commands import Database

from states.main_bot import Statistics


async def all_statistics_time_line(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    texts = await load_texts()

    now = datetime.now(tz=TZ).strftime("%d.%m.%Y")
    await state.set_state(Statistics.allPeriod)
    await callback.message.delete()
    await callback.message.answer(text=texts['input_period'].format(date=now),
                                  reply_markup=await InlineKeyboardMain.back("admin_statistics"))


async def all_get_period(message: Message, state: FSMContext):
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

    shops = await Database.MainBot.get_all_shops()
    profit = sum([await Database.MainBot.get_profit(shop.id, start, end) for shop in shops])
    sales = sum([await Database.MainBot.get_sales(shop.id, start, end) for shop in shops])
    users = sum([await Database.MainBot.get_users_shop(shop.id, start, end) for shop in shops])

    await message.answer(text=texts['allPeriodStatistics'].format(profit=profit,
                                                                  sales=sales,
                                                                  users=users,
                                                                  date=message.text),
                         reply_markup=await InlineKeyboardMain.back("admin_all_statistics_time_line"))
